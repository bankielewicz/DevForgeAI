# Upgrade Services API Reference (STORY-078)

Quick reference guide for using the upgrade management services.

## Quick Start

```python
from installer.upgrade_orchestrator import UpgradeOrchestrator
from pathlib import Path

# Initialize orchestrator (uses default services)
orchestrator = UpgradeOrchestrator()

# Detect upgrade
result = orchestrator.detect_upgrade("1.0.0", "1.1.0")
if result['is_upgrade']:
    print(f"Upgrade available: {result['message']}")

# Execute complete upgrade workflow
summary = orchestrator.execute(
    from_version="1.0.0",
    to_version="1.1.0",
    source_root=Path("/path/to/new/version"),
    target_root=Path("/path/to/current/installation")
)

if summary.status.SUCCESS:
    print(f"Upgrade complete in {summary.duration_seconds:.1f}s")
    print(f"Backup: {summary.backup_path}")
else:
    print(f"Upgrade failed: {summary.error_message}")
```

## Services

### BackupService

**Purpose:** Create, restore, and manage installation backups.

```python
from installer.backup_service import BackupService
from installer.models import BackupReason
from pathlib import Path

service = BackupService(backups_root=Path("devforgeai/backups"))

# Create backup
metadata = service.create_backup(
    source_root=Path("."),
    version="1.0.0",
    reason=BackupReason.UPGRADE  # or UNINSTALL, MANUAL
)

# List backups
backups = service.list_backups()
for backup in backups:
    print(f"Backup: {backup.backup_id} ({backup.version})")

# Restore from backup
service.restore(backup_id="v1.0.0-20251205-143022-001", target_root=Path("."))

# Cleanup old backups (keep 5 most recent)
deleted_count = service.cleanup(retention_count=5)
print(f"Deleted {deleted_count} old backup(s)")
```

**Performance:**
- Backup creation: <30 seconds for typical installation
- Restoration: <60 seconds
- Throughput: ~50MB/second on SSD

**Excluded Directories:**
- `.git/`, `__pycache__/`, `.pytest_cache/`, `.venv/`, `node_modules/`
- `devforgeai/backups/` (prevents backup recursion)

### MigrationDiscovery

**Purpose:** Find and order applicable migration scripts.

```python
from installer.migration_discovery import MigrationDiscovery
from pathlib import Path

discovery = MigrationDiscovery(migrations_dir=Path("migrations"))

# Discover migrations from 1.0.0 to 1.2.0
# Automatically includes intermediate migrations:
# v1.0.0-to-v1.1.0.py → v1.1.0-to-v1.2.0.py
migrations = discovery.discover(
    from_version="1.0.0",
    to_version="1.2.0"
)

for migration in migrations:
    print(f"Migration: {migration.from_version} → {migration.to_version}")
    print(f"Script: {migration.path}")

# If no path exists, returns empty list and logs warnings
```

**Convention:**
- Migration files must be named: `vX.Y.Z-to-vA.B.C.py`
- Stored in `migrations/` directory
- Must be executable Python scripts

**Pathfinding:**
- Uses breadth-first search (BFS)
- Finds shortest path through migration chains
- Logs warnings for gaps (missing intermediate migrations)

### MigrationRunner

**Purpose:** Execute migration scripts in sequence with output capture.

```python
from installer.migration_runner import MigrationRunner

runner = MigrationRunner(python_executable="/usr/bin/python3")

# Execute migrations
run_result = runner.run(
    migrations=migrations,
    timeout_seconds=300  # 5 minutes per migration
)

if run_result.all_success:
    print(f"All {run_result.applied_count} migrations completed")
else:
    print(f"Migration failed at step {run_result.applied_count + 1}")
    print(f"Error: {run_result.failed_migration_result.error_message}")
    print(f"Output: {run_result.failed_migration_result.stdout}")
    print(f"Errors: {run_result.failed_migration_result.stderr}")

# Get list of applied migrations for rollback reference
applied = runner.get_applied_migrations(run_result)
```

**Behavior:**
- Executes migrations as subprocesses
- Captures both stdout and stderr
- Stops on first failure (doesn't continue)
- Respects timeout (default 300 seconds)
- Tracks successfully applied migrations

**Exit Codes:**
- 0 = Success
- Non-zero = Failure (triggers rollback)

### MigrationValidator

**Purpose:** Validate post-migration installation state.

```python
from installer.migration_validator import MigrationValidator
from pathlib import Path

validator = MigrationValidator()

report = validator.validate(
    root_path=Path("."),

    # Check that expected files exist
    expected_files=[
        ".claude/skills/devforgeai-qa/SKILL.md",
        "devforgeai/specs/context/tech-stack.md",
        "CLAUDE.md"
    ],

    # Check that expected directories exist
    expected_dirs=[
        ".claude/skills",
        "devforgeai/context"
    ],

    # Validate JSON files have required keys
    json_schemas={
        "devforgeai/.version.json": ["version", "installed_at"],
        "devforgeai/config/upgrade-config.json": [
            "backup_retention_count",
            "migration_timeout_seconds"
        ]
    },

    # Same as json_schemas (for config validation)
    config_validations={
        "devforgeai/.version.json": ["version", "upgraded_from"]
    }
)

# Check results
if report.is_valid:
    print(f"Validation passed ({report.passed_checks}/{report.total_checks})")
else:
    print(f"Validation failed: {report.failed_checks} checks failed")
    for check in report.checks:
        if not check.passed:
            print(f"  ✗ {check.name}: {check.message}")
```

**Supported Checks:**
- File existence
- Directory existence
- JSON well-formedness
- YAML well-formedness
- Required configuration keys
- Nested key validation (e.g., "settings.debug")

**Return Value:**
- `ValidationReport` with individual check results
- Each check has name, pass/fail status, message, and details

### UpgradeOrchestrator

**Purpose:** Coordinate the complete upgrade workflow.

```python
from installer.upgrade_orchestrator import UpgradeOrchestrator
from pathlib import Path

orchestrator = UpgradeOrchestrator()

# Step 1: Detect upgrade
detection = orchestrator.detect_upgrade(
    installed_version="1.0.0",
    package_version="1.1.0"
)

if not detection['is_upgrade']:
    print("No upgrade needed")
    exit(0)

print(f"Upgrade type: {detection['upgrade_type']}")  # major, minor, or patch

# Step 2: Execute upgrade (includes everything)
summary = orchestrator.execute(
    from_version="1.0.0",
    to_version="1.1.0",
    source_root=Path("/tmp/devforgeai-1.1.0"),  # New version files
    target_root=Path("."),  # Current installation
    migrations_dir=Path("migrations"),
    migration_timeout_seconds=300,
    backup_retention_count=5
)

# Step 3: Check results
print(f"Status: {summary.status.name}")
print(f"Duration: {summary.duration_seconds:.1f}s")
print(f"Backup: {summary.backup_path}")
print(f"Migrations: {len(summary.migrations_applied)}")

if summary.status == UpgradeStatus.SUCCESS:
    print("✓ Upgrade completed successfully")
elif summary.status == UpgradeStatus.ROLLED_BACK:
    print("⚠ Upgrade failed and was rolled back")
    print(f"Error: {summary.error_message}")
else:
    print("✗ Upgrade failed without rollback")
    print(f"Error: {summary.error_message}")
```

**Workflow (automatic):**
1. Create backup (atomic, before any changes)
2. Discover applicable migrations
3. Execute migrations in order
4. Validate post-migration state
5. Update version metadata
6. Cleanup old backups

**On Failure (automatic):**
1. Restore from backup
2. Restore version metadata
3. Generate error summary
4. Return ROLLED_BACK status

**Return Value:**
- `UpgradeSummary` with:
  - Status: SUCCESS, FAILED, or ROLLED_BACK
  - File counts and lists (added, updated, removed)
  - Migrations applied
  - Backup location
  - Duration
  - Error message (if failed)

## Data Models

### BackupMetadata

```python
@dataclass(frozen=True)
class BackupMetadata:
    backup_id: str                    # v1.0.0-20251205-143022-001
    version: str                      # 1.0.0
    created_at: str                   # ISO8601 timestamp
    files: List[FileEntry]            # List of backed-up files
    reason: BackupReason              # UPGRADE, UNINSTALL, MANUAL
    duration_seconds: Optional[float]  # Backup time
```

### ValidationReport

```python
@dataclass(frozen=True)
class ValidationReport:
    is_valid: bool                    # All checks passed?
    checks: List[ValidationCheck]     # Individual check results
    total_checks: int                 # Total checks run
    passed_checks: int                # Checks that passed
    failed_checks: int                # Checks that failed
```

### UpgradeSummary

```python
@dataclass(frozen=True)
class UpgradeSummary:
    from_version: str
    to_version: str
    status: UpgradeStatus              # SUCCESS, FAILED, ROLLED_BACK
    files_added: int
    files_updated: int
    files_removed: int
    files_added_list: List[str]
    files_updated_list: List[str]
    files_removed_list: List[str]
    migrations_applied: List[str]
    backup_path: Optional[str]
    duration_seconds: float
    error_message: Optional[str]
```

## Exception Handling

```python
from installer.models import (
    UpgradeError,
    BackupError,
    MigrationError,
    ValidationError,
    RollbackError
)

try:
    orchestrator.execute(from_version, to_version, source, target)
except BackupError as e:
    print(f"Backup failed: {e}")
except MigrationError as e:
    print(f"Migration failed: {e}")
except ValidationError as e:
    print(f"Validation failed: {e}")
except RollbackError as e:
    print(f"Rollback failed: {e}")
except UpgradeError as e:
    print(f"Upgrade error: {e}")
```

All exceptions include context and error messages suitable for logging and user display.

## Configuration

Load configuration from `upgrade-config.json`:

```python
import json

config = json.loads(Path("devforgeai/config/upgrade-config.json").read_text())

orchestrator.execute(
    from_version="1.0.0",
    to_version="1.1.0",
    source_root=source,
    target_root=target,
    migrations_dir=Path(config["migration_script_directory"]),
    migration_timeout_seconds=config["migration_timeout_seconds"],
    backup_retention_count=config["backup_retention_count"]
)
```

## Logging

Enable debug logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

orchestrator.execute(...)  # Now outputs debug information
```

Log messages include:
- Backup creation progress
- Migration discovery details
- Migration execution output
- Validation results
- Rollback operations
- Error context

## Testing

### Mock Services for Testing

```python
from unittest.mock import MagicMock
from installer.backup_service import IBackupService

mock_backup = MagicMock(spec=IBackupService)
mock_backup.create_backup.return_value = mock_metadata

orchestrator = UpgradeOrchestrator(
    backup_service=mock_backup
)
```

### Using pytest Fixtures

```python
def test_upgrade(tmp_path):
    source = tmp_path / "source"
    target = tmp_path / "target"
    source.mkdir()
    target.mkdir()

    orchestrator = UpgradeOrchestrator()
    summary = orchestrator.execute(
        from_version="1.0.0",
        to_version="1.1.0",
        source_root=source,
        target_root=target
    )

    assert summary.status == UpgradeStatus.SUCCESS
```

## Troubleshooting

### Backup Creation Fails

- **Insufficient disk space**: Ensure target disk has 2x the installation size
- **Permission denied**: Check write permissions on `devforgeai/backups/`
- **Timeout**: Installation >50MB may take >30s (increase timeout)

### Migration Not Found

- **Convention mismatch**: Ensure `vX.Y.Z-to-vA.B.C.py` naming
- **Wrong directory**: Check `migrations_dir` parameter
- **Path issue**: Migration file must exist on filesystem

### Validation Failures

- **Missing files**: New version missing expected files
- **Invalid JSON**: Configuration file syntax error
- **Missing keys**: Configuration missing required key

### Rollback Fails

- **Backup corrupted**: Checksum mismatch during restore
- **Disk full**: Insufficient space to restore all files
- **Permission denied**: Cannot restore to target location

## Performance Tips

1. **Parallel backups** - Not supported, but could be added
2. **Incremental migrations** - Use migration chains instead of large single migrations
3. **Validate early** - Fail fast on validation errors
4. **Monitor disk space** - Upgrade uses 2x space (backup + new files)
5. **Test migrations** - Run migration tests before upgrade

## Reference

- `installer/models.py` - Data models and exceptions
- `installer/backup_service.py` - Backup operations
- `installer/migration_discovery.py` - Migration discovery
- `installer/migration_runner.py` - Migration execution
- `installer/migration_validator.py` - Validation
- `installer/upgrade_orchestrator.py` - Orchestration
- `devforgeai/config/upgrade-config.json` - Configuration template
