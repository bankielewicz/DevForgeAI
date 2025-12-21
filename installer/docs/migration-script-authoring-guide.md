# Migration Script Authoring Guide

Guide for creating DevForgeAI migration scripts that execute during version upgrades.

---

## Overview

Migration scripts automate changes between DevForgeAI versions. They handle:
- File moves and renames
- Configuration updates
- Schema changes
- Deprecation handling

---

## Naming Convention

Migration scripts MUST follow this naming pattern:

```
vX.Y.Z-to-vA.B.C.py
```

**Examples:**
- `v1.0.0-to-v1.1.0.py` - Minor version upgrade
- `v1.1.0-to-v1.2.0.py` - Another minor upgrade
- `v1.2.0-to-v2.0.0.py` - Major version upgrade

**Rules:**
- Use lowercase `v` prefix
- Use semantic versioning (X.Y.Z)
- Use `-to-` separator
- File extension must be `.py`

---

## Script Structure

Every migration script must implement the `migrate()` function:

```python
"""
Migration: v1.0.0 to v1.1.0

Changes:
- Moves config from old location to new
- Updates schema version in settings
"""

from pathlib import Path
import json
import shutil


def migrate(project_root: Path, dry_run: bool = False) -> dict:
    """
    Execute migration from v1.0.0 to v1.1.0.

    Args:
        project_root: Path to project root directory
        dry_run: If True, validate without making changes

    Returns:
        dict with keys:
            - status: "success" | "failed" | "dry_run_validated"
            - files_moved: List of (old_path, new_path) tuples
            - files_updated: List of updated file paths
            - files_created: List of new file paths
            - files_deleted: List of removed file paths
            - error: Error message if failed (optional)
    """
    result = {
        "status": "success",
        "files_moved": [],
        "files_updated": [],
        "files_created": [],
        "files_deleted": [],
    }

    try:
        # Example: Move config file
        old_config = project_root / "devforgeai" / "old-config.json"
        new_config = project_root / "devforgeai" / "config" / "settings.json"

        if old_config.exists():
            if dry_run:
                result["status"] = "dry_run_validated"
            else:
                new_config.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_config), str(new_config))
                result["files_moved"].append((str(old_config), str(new_config)))

        # Example: Update schema version
        version_file = project_root / "devforgeai" / ".version.json"
        if version_file.exists():
            if dry_run:
                result["status"] = "dry_run_validated"
            else:
                data = json.loads(version_file.read_text())
                data["schema_version"] = "2.0"
                version_file.write_text(json.dumps(data, indent=2))
                result["files_updated"].append(str(version_file))

    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)

    return result
```

---

## Return Value Schema

The `migrate()` function must return a dictionary with these keys:

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `status` | str | Yes | "success", "failed", or "dry_run_validated" |
| `files_moved` | List[Tuple[str, str]] | Yes | List of (old_path, new_path) |
| `files_updated` | List[str] | Yes | List of modified file paths |
| `files_created` | List[str] | Yes | List of new file paths |
| `files_deleted` | List[str] | Yes | List of removed file paths |
| `error` | str | No | Error message if status is "failed" |

---

## Best Practices

### 1. Idempotency

Scripts should be safe to run multiple times:

```python
def migrate(project_root: Path, dry_run: bool = False) -> dict:
    result = {"status": "success", "files_moved": [], ...}

    old_file = project_root / "old-location" / "file.txt"
    new_file = project_root / "new-location" / "file.txt"

    # Check if migration already done
    if new_file.exists() and not old_file.exists():
        # Already migrated - nothing to do
        return result

    # Proceed with migration...
```

### 2. Dry Run Support

Always implement dry_run mode for safe validation:

```python
if dry_run:
    # Validate prerequisites exist
    if not old_file.exists():
        result["status"] = "failed"
        result["error"] = f"Required file not found: {old_file}"
        return result
    result["status"] = "dry_run_validated"
    return result

# Actual migration...
```

### 3. Error Handling

Catch exceptions and return structured errors:

```python
try:
    # Migration logic
    shutil.move(str(old_file), str(new_file))
except PermissionError as e:
    result["status"] = "failed"
    result["error"] = f"Permission denied: {e}"
except FileNotFoundError as e:
    result["status"] = "failed"
    result["error"] = f"File not found: {e}"
except Exception as e:
    result["status"] = "failed"
    result["error"] = f"Unexpected error: {e}"
```

### 4. Atomic Operations

Use temporary files for complex updates:

```python
import tempfile

def update_config_safely(config_path: Path, updates: dict):
    """Update config file atomically."""
    # Read existing
    data = json.loads(config_path.read_text())
    data.update(updates)

    # Write to temp file first
    with tempfile.NamedTemporaryFile(
        mode='w',
        dir=config_path.parent,
        delete=False,
        suffix='.tmp'
    ) as tmp:
        json.dump(data, tmp, indent=2)
        tmp_path = Path(tmp.name)

    # Atomic rename
    tmp_path.replace(config_path)
```

---

## Migration Types

### File Moves

```python
# Move single file
shutil.move(str(old_path), str(new_path))

# Move directory
shutil.move(str(old_dir), str(new_dir))

# Copy then delete (safer for cross-filesystem moves)
shutil.copy2(str(old_path), str(new_path))
old_path.unlink()
```

### Configuration Updates

```python
# JSON config
config = json.loads(config_path.read_text())
config["new_key"] = "value"
del config["deprecated_key"]
config_path.write_text(json.dumps(config, indent=2))

# YAML config (if PyYAML available)
try:
    import yaml
    config = yaml.safe_load(config_path.read_text())
    config["new_key"] = "value"
    config_path.write_text(yaml.dump(config))
except ImportError:
    # Fallback to string manipulation
    pass
```

### Schema Changes

```python
def upgrade_schema_v1_to_v2(data: dict) -> dict:
    """Convert schema from v1 to v2 format."""
    return {
        "schema_version": "2.0",
        "settings": {
            "option_a": data.get("optionA"),  # Renamed
            "option_b": data.get("optionB"),
            "new_option": "default_value",    # Added
        },
        # "old_field" removed
    }
```

### Deprecation Handling

```python
def handle_deprecated_features(project_root: Path) -> list:
    """Remove deprecated files and configs."""
    removed = []

    deprecated_files = [
        "devforgeai/deprecated-feature.json",
        ".claude/old-command.md",
    ]

    for rel_path in deprecated_files:
        file_path = project_root / rel_path
        if file_path.exists():
            file_path.unlink()
            removed.append(str(file_path))

    return removed
```

---

## Testing Migrations

### Unit Test Template

```python
import pytest
from pathlib import Path
import json

def test_migration_v1_0_0_to_v1_1_0(tmp_path):
    """Test v1.0.0 to v1.1.0 migration."""
    # Arrange: Create v1.0.0 structure
    old_config = tmp_path / "devforgeai" / "old-config.json"
    old_config.parent.mkdir(parents=True)
    old_config.write_text('{"key": "value"}')

    # Act: Run migration
    from installer.migrations.v1_0_0_to_v1_1_0 import migrate
    result = migrate(tmp_path, dry_run=False)

    # Assert
    assert result["status"] == "success"
    assert not old_config.exists()
    new_config = tmp_path / "devforgeai" / "config" / "settings.json"
    assert new_config.exists()


def test_migration_dry_run(tmp_path):
    """Test dry run doesn't modify files."""
    old_config = tmp_path / "devforgeai" / "old-config.json"
    old_config.parent.mkdir(parents=True)
    old_config.write_text('{"key": "value"}')

    from installer.migrations.v1_0_0_to_v1_1_0 import migrate
    result = migrate(tmp_path, dry_run=True)

    assert result["status"] == "dry_run_validated"
    assert old_config.exists()  # Not moved
```

---

## Troubleshooting

### Common Issues

**Migration not discovered:**
- Check filename matches `vX.Y.Z-to-vA.B.C.py` pattern exactly
- Ensure file is in `installer/migrations/` directory
- Verify version numbers are valid semver

**Migration fails silently:**
- Always return error details in result["error"]
- Log important operations for debugging
- Check file permissions

**Rollback not working:**
- Ensure backup was created before migration started
- Check backup contains all affected files
- Verify rollback service has read access to backup

---

## Example Migrations

See `installer/migrations/` for example scripts:
- `v0.0.0-to-v0.0.1.py` - Simple example migration

---

**Version:** 1.0
**Last Updated:** 2025-12-06
**Story:** STORY-078
