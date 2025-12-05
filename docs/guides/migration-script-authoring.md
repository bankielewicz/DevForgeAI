# Migration Script Authoring Guide

## Overview

This guide explains how to write migration scripts for DevForgeAI version upgrades. Migration scripts automate the process of updating DevForgeAI installations from one version to another, handling file moves, configuration updates, schema changes, and deprecation handling.

## Purpose

Migration scripts enable:
- Automated file reorganization during upgrades
- Configuration key updates and transformations
- Data model format migrations
- Deprecation handling and feature removal
- Safe, repeatable upgrade paths between versions

## File Naming Convention

Migration scripts follow this naming convention:

```
migrations/vX.Y.Z-to-vA.B.C.py
```

**Examples:**
- `migrations/v1.0.0-to-v1.1.0.py`
- `migrations/v1.1.0-to-v1.2.0.py`
- `migrations/v2.0.0-to-v2.1.0.py`

**Rules:**
- Use lowercase `v` prefix
- Use semantic versioning (major.minor.patch)
- Use `-to-` separator between versions
- Extensions must be `.py`
- Filename must exactly match versions being migrated

## Required Script Structure

Every migration script must follow this structure:

```python
#!/usr/bin/env python3
"""
Migration from vX.Y.Z to vA.B.C

Description: Brief explanation of what this migration does.
This migration handles:
- File move 1
- Configuration update 2
- Schema change 3
"""

import os
import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Tuple

# Set up logging
logger = logging.getLogger(__name__)


def main() -> int:
    """
    Execute migration from vX.Y.Z to vA.B.C.

    Returns:
        0 if successful
        1 if failed (triggers rollback)
    """
    try:
        logger.info("Starting migration from vX.Y.Z to vA.B.C")

        # Phase 1: Validation
        if not validate_preconditions():
            logger.error("Preconditions not met")
            return 1

        # Phase 2: Perform migrations
        if not perform_migrations():
            logger.error("Migration failed")
            return 1

        # Phase 3: Validation
        if not validate_postconditions():
            logger.error("Postconditions not met")
            return 1

        logger.info("Migration completed successfully")
        return 0

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


def validate_preconditions() -> bool:
    """
    Validate that migration can proceed.

    Checks:
    - Current version matches expected version
    - Required files exist
    - Sufficient disk space

    Returns:
        True if all preconditions met, False otherwise
    """
    try:
        # Check if required files exist
        if not Path(".devforgeai/context/tech-stack.md").exists():
            logger.error("Required file not found: .devforgeai/context/tech-stack.md")
            return False

        logger.info("Preconditions validated")
        return True

    except Exception as e:
        logger.error(f"Precondition validation failed: {e}")
        return False


def perform_migrations() -> bool:
    """
    Execute actual migration operations.

    Handles:
    - File moves
    - Configuration updates
    - Schema changes
    - Deprecation handling

    Returns:
        True if all operations successful, False otherwise
    """
    try:
        # Example: Move files
        # if not move_files():
        #     return False

        # Example: Update configurations
        # if not update_configurations():
        #     return False

        logger.info("All migration operations completed")
        return True

    except Exception as e:
        logger.error(f"Migration operations failed: {e}")
        return False


def validate_postconditions() -> bool:
    """
    Validate migration success.

    Checks:
    - Expected files exist at new locations
    - Configuration valid
    - No data corruption

    Returns:
        True if all postconditions met, False otherwise
    """
    try:
        # Check if expected files exist
        # if not Path("new/location/file.txt").exists():
        #     logger.error("Expected file not found after migration")
        #     return False

        logger.info("Postconditions validated")
        return True

    except Exception as e:
        logger.error(f"Postcondition validation failed: {e}")
        return False


if __name__ == "__main__":
    exit(main())
```

## Phase 1: File Operations

### Moving Files

```python
def move_files() -> bool:
    """Move files to new locations during upgrade."""
    try:
        # Define file movements
        moves = {
            "old/path/file.md": "new/path/file.md",
            ".claude/agents/old-agent.md": ".claude/agents/new-agent.md",
        }

        for src, dst in moves.items():
            src_path = Path(src)
            dst_path = Path(dst)

            # Create destination directory if needed
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Move file
            if src_path.exists():
                shutil.move(str(src_path), str(dst_path))
                logger.info(f"Moved: {src} → {dst}")
            else:
                logger.warning(f"Source file not found (skipping): {src}")

        return True

    except Exception as e:
        logger.error(f"File move failed: {e}")
        return False
```

### Deleting Files

```python
def delete_files() -> bool:
    """Delete deprecated files."""
    try:
        # Define files to delete
        files_to_delete = [
            ".claude/agents/old-deprecated-agent.md",
            ".devforgeai/old-config.json",
        ]

        for file_path in files_to_delete:
            p = Path(file_path)
            if p.exists():
                if p.is_file():
                    p.unlink()
                elif p.is_dir():
                    shutil.rmtree(p)
                logger.info(f"Deleted: {file_path}")
            else:
                logger.warning(f"File not found (skipping): {file_path}")

        return True

    except Exception as e:
        logger.error(f"File deletion failed: {e}")
        return False
```

### Creating Files

```python
def create_files() -> bool:
    """Create new files required by new version."""
    try:
        # Define new files
        new_files = {
            ".devforgeai/config/new-config.json": {
                "version": "1.1.0",
                "features": ["new_feature_1", "new_feature_2"]
            }
        }

        for file_path, content in new_files.items():
            p = Path(file_path)
            p.parent.mkdir(parents=True, exist_ok=True)

            if isinstance(content, dict):
                with open(p, 'w') as f:
                    json.dump(content, f, indent=2)
            else:
                with open(p, 'w') as f:
                    f.write(content)

            logger.info(f"Created: {file_path}")

        return True

    except Exception as e:
        logger.error(f"File creation failed: {e}")
        return False
```

## Phase 2: Configuration Updates

### Updating JSON Configuration

```python
def update_json_config() -> bool:
    """Update JSON configuration files."""
    try:
        config_path = Path(".devforgeai/config/upgrade-config.json")

        if not config_path.exists():
            logger.warning("Configuration file not found, skipping update")
            return True

        # Load existing config
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Update/add keys
        config["new_key"] = "new_value"
        config["backup_retention_count"] = 5

        # Remove deprecated keys if needed
        if "old_deprecated_key" in config:
            del config["old_deprecated_key"]
            logger.info("Removed deprecated key: old_deprecated_key")

        # Write updated config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        logger.info("Configuration updated successfully")
        return True

    except Exception as e:
        logger.error(f"Configuration update failed: {e}")
        return False
```

### Updating Text Files

```python
def update_text_file_content(file_path: str, old_text: str, new_text: str) -> bool:
    """Replace text in configuration files."""
    try:
        p = Path(file_path)

        if not p.exists():
            logger.warning(f"File not found: {file_path}")
            return True

        # Read original content
        with open(p, 'r') as f:
            content = f.read()

        # Replace text
        if old_text in content:
            content = content.replace(old_text, new_text)

            # Write updated content
            with open(p, 'w') as f:
                f.write(content)

            logger.info(f"Updated file: {file_path}")
        else:
            logger.warning(f"Pattern not found in {file_path}")

        return True

    except Exception as e:
        logger.error(f"File update failed: {e}")
        return False
```

## Phase 3: Schema Changes

### Updating Data Models

```python
def update_data_models() -> bool:
    """Update story and epic files for schema changes."""
    try:
        stories_dir = Path(".ai_docs/Stories")

        if not stories_dir.exists():
            logger.info("Stories directory not found, skipping data model updates")
            return True

        # Iterate through all story files
        for story_file in stories_dir.glob("*.story.md"):
            if not update_story_schema(story_file):
                return False

        logger.info("Data model updates completed")
        return True

    except Exception as e:
        logger.error(f"Data model update failed: {e}")
        return False


def update_story_schema(file_path: Path) -> bool:
    """Update individual story schema."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Example: Update format_version
        if 'format_version: "2.0"' in content:
            content = content.replace('format_version: "2.0"', 'format_version: "2.1"')

            with open(file_path, 'w') as f:
                f.write(content)

            logger.info(f"Updated schema: {file_path.name}")

        return True

    except Exception as e:
        logger.error(f"Story schema update failed for {file_path}: {e}")
        return False
```

## Phase 4: Deprecation Handling

### Removing Deprecated Features

```python
def handle_deprecations() -> bool:
    """Remove deprecated features and update references."""
    try:
        # Remove deprecated agent files
        deprecated_agents = [
            ".claude/agents/old-agent-v1.md",
            ".claude/agents/deprecated-skill.md",
        ]

        for agent_path in deprecated_agents:
            p = Path(agent_path)
            if p.exists():
                p.unlink()
                logger.info(f"Removed deprecated: {agent_path}")

        # Update CLAUDE.md to remove references
        claude_path = Path("CLAUDE.md")
        if claude_path.exists():
            with open(claude_path, 'r') as f:
                content = f.read()

            # Remove deprecated section
            if "## Deprecated Features" in content:
                # Remove deprecation section
                lines = content.split('\n')
                start = next((i for i, line in enumerate(lines) if "## Deprecated Features" in line), -1)
                if start >= 0:
                    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('##')), len(lines))
                    content = '\n'.join(lines[:start] + lines[end:])

                    with open(claude_path, 'w') as f:
                        f.write(content)

                    logger.info("Removed deprecated features section from CLAUDE.md")

        return True

    except Exception as e:
        logger.error(f"Deprecation handling failed: {e}")
        return False
```

## Error Handling Best Practices

### Validation Pattern

```python
def safe_operation(operation_name: str, operation_func) -> bool:
    """Wrapper for safe migration operations with logging."""
    try:
        logger.info(f"Starting: {operation_name}")
        result = operation_func()
        logger.info(f"Completed: {operation_name}")
        return result
    except Exception as e:
        logger.error(f"Failed {operation_name}: {e}")
        return False
```

### Checking File Existence

```python
def require_file(file_path: str, context: str = "") -> bool:
    """Ensure required file exists."""
    p = Path(file_path)
    if not p.exists():
        logger.error(f"Required file missing: {file_path}" +
                    (f" ({context})" if context else ""))
        return False
    return True
```

### Checking Disk Space

```python
import shutil

def check_disk_space(required_mb: int) -> bool:
    """Verify sufficient disk space available."""
    stat = shutil.disk_usage("/")
    available_mb = stat.free / (1024 * 1024)

    if available_mb < required_mb:
        logger.error(f"Insufficient disk space: {available_mb:.0f}MB available, "
                    f"{required_mb}MB required")
        return False

    logger.info(f"Disk space check passed: {available_mb:.0f}MB available")
    return True
```

## Testing Migration Scripts

### Local Testing

```bash
# Test migration script directly
cd /path/to/DevForgeAI
python3 migrations/v1.0.0-to-v1.1.0.py

# With verbose logging
python3 -u migrations/v1.0.0-to-v1.1.0.py 2>&1 | tee migration.log
```

### Test Fixtures

Create test migrations in `tests/migrations/fixtures/`:

```python
# tests/migrations/test_v1_0_0_to_v1_1_0.py

import pytest
from pathlib import Path
import tempfile
import shutil
import sys

@pytest.fixture
def migration_env(tmp_path):
    """Set up test environment for migration."""
    # Create DevForgeAI directory structure
    devforgeai_dir = tmp_path / ".devforgeai"
    devforgeai_dir.mkdir()

    # Create required subdirectories
    (devforgeai_dir / "context").mkdir()
    (devforgeai_dir / "config").mkdir()

    # Create test files
    (devforgeai_dir / "context" / "tech-stack.md").write_text("# Tech Stack\n")

    # Change to test directory
    original_cwd = Path.cwd()
    import os
    os.chdir(tmp_path)

    yield tmp_path

    # Restore original directory
    os.chdir(original_cwd)


def test_migration_success(migration_env):
    """Test successful migration."""
    # Import and run migration
    sys.path.insert(0, str(Path.cwd() / "migrations"))
    from v1_0_0_to_v1_1_0 import main

    result = main()
    assert result == 0

    # Verify expected files
    assert (migration_env / "new_path" / "file.md").exists()


def test_migration_missing_precondition(migration_env):
    """Test migration with missing preconditions."""
    # Remove required file
    (migration_env / ".devforgeai" / "context" / "tech-stack.md").unlink()

    sys.path.insert(0, str(Path.cwd() / "migrations"))
    from v1_0_0_to_v1_1_0 import main

    result = main()
    assert result == 1  # Should fail
```

## Example: Simple Migration

**File:** `migrations/v1.0.0-to-v1.1.0.py`

This migration renames `.claude/agents/old-agent.md` to `.claude/agents/new-agent.md`:

```python
#!/usr/bin/env python3
"""
Migration from v1.0.0 to v1.1.0

Renames agents as part of internal reorganization.
"""

import os
import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def main() -> int:
    """Execute migration."""
    try:
        logger.info("Starting migration from v1.0.0 to v1.1.0")

        # Define file moves
        moves = {
            ".claude/agents/test-automator.md": ".claude/agents/test-automation-engine.md",
            ".claude/agents/api-designer.md": ".claude/agents/api-specification-designer.md",
        }

        for src, dst in moves.items():
            src_path = Path(src)
            dst_path = Path(dst)

            if src_path.exists():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src_path), str(dst_path))
                logger.info(f"Renamed: {src} → {dst}")
            else:
                logger.warning(f"Source file not found (skipping): {src}")

        logger.info("Migration completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return 1


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    exit(main())
```

## Example: Complex Migration

**File:** `migrations/v1.1.0-to-v1.2.0.py`

This migration handles file moves, configuration updates, and schema changes:

```python
#!/usr/bin/env python3
"""
Migration from v1.1.0 to v1.2.0

Handles:
- Moving stories to new directory structure
- Updating story schema from v2.0 to v2.1
- Creating new configuration file
- Removing deprecated agents
"""

import os
import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


def main() -> int:
    """Execute migration."""
    try:
        logger.info("Starting migration from v1.1.0 to v1.2.0")

        if not validate_preconditions():
            return 1

        if not perform_migrations():
            return 1

        if not validate_postconditions():
            return 1

        logger.info("Migration completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


def validate_preconditions() -> bool:
    """Validate migration can proceed."""
    required_files = [
        ".devforgeai/context/tech-stack.md",
        ".ai_docs/Stories",
    ]

    for file_path in required_files:
        if not Path(file_path).exists():
            logger.error(f"Required file/directory not found: {file_path}")
            return False

    logger.info("Preconditions validated")
    return True


def perform_migrations() -> bool:
    """Execute migration operations."""
    operations = [
        ("Removing deprecated agents", remove_deprecated_agents),
        ("Updating story schema", update_story_schema),
        ("Creating new configuration", create_new_configuration),
        ("Moving archived stories", move_archived_stories),
    ]

    for operation_name, operation_func in operations:
        try:
            logger.info(f"Starting: {operation_name}")
            if not operation_func():
                logger.error(f"Failed: {operation_name}")
                return False
            logger.info(f"Completed: {operation_name}")
        except Exception as e:
            logger.error(f"Error during {operation_name}: {e}")
            return False

    return True


def remove_deprecated_agents() -> bool:
    """Remove deprecated agent files."""
    deprecated = [
        ".claude/agents/old-pattern-detector.md",
        ".claude/agents/legacy-skill-manager.md",
    ]

    for agent_path in deprecated:
        p = Path(agent_path)
        if p.exists():
            p.unlink()
            logger.info(f"Deleted: {agent_path}")
        else:
            logger.warning(f"Not found (skipping): {agent_path}")

    return True


def update_story_schema() -> bool:
    """Update all stories from v2.0 to v2.1 format."""
    stories_dir = Path(".ai_docs/Stories")

    if not stories_dir.exists():
        logger.warning("Stories directory not found")
        return True

    for story_file in stories_dir.glob("*.story.md"):
        try:
            with open(story_file, 'r') as f:
                content = f.read()

            # Update schema version
            content = content.replace(
                'format_version: "2.0"',
                'format_version: "2.1"'
            )

            with open(story_file, 'w') as f:
                f.write(content)

            logger.info(f"Updated schema for: {story_file.name}")

        except Exception as e:
            logger.error(f"Failed to update {story_file}: {e}")
            return False

    return True


def create_new_configuration() -> bool:
    """Create new configuration file for v1.2.0 features."""
    config_path = Path(".devforgeai/config/new-features.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)

    config = {
        "version": "1.2.0",
        "features": {
            "parallel_migration": True,
            "dry_run_mode": True,
            "migration_hooks": []
        }
    }

    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        logger.info(f"Created configuration: {config_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to create configuration: {e}")
        return False


def move_archived_stories() -> bool:
    """Move archived stories to new location."""
    try:
        archive_src = Path(".ai_docs/Stories/archive")
        archive_dst = Path(".ai_docs/archive/stories")

        if archive_src.exists():
            archive_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(archive_src), str(archive_dst))
            logger.info(f"Moved archive: {archive_src} → {archive_dst}")

        return True

    except Exception as e:
        logger.error(f"Failed to move archive: {e}")
        return False


def validate_postconditions() -> bool:
    """Validate migration success."""
    # Check that new format files exist
    expected_files = [
        ".devforgeai/config/new-features.json",
    ]

    for file_path in expected_files:
        if not Path(file_path).exists():
            logger.error(f"Expected file not found: {file_path}")
            return False

    # Verify deprecated files removed
    deprecated_files = [
        ".claude/agents/old-pattern-detector.md",
    ]

    for file_path in deprecated_files:
        if Path(file_path).exists():
            logger.warning(f"Deprecated file still exists: {file_path}")

    logger.info("Postconditions validated")
    return True


if __name__ == "__main__":
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    exit(main())
```

## Best Practices

### 1. **Idempotency**
Write migrations that can be run multiple times safely:

```python
# Good: Check before moving
if src_path.exists():
    shutil.move(str(src_path), str(dst_path))

# Avoid: Assuming file exists
shutil.move(str(src_path), str(dst_path))  # May fail on retry
```

### 2. **Comprehensive Logging**
Log all operations for debugging and audit trails:

```python
logger.info(f"Starting migration from {from_version} to {to_version}")
logger.debug(f"File count: {len(files)}")
logger.warning(f"File not found (skipping): {file_path}")
logger.error(f"Migration failed: {reason}")
```

### 3. **Exit Codes**
Always return meaningful exit codes:
- `0` = Success
- `1` = Failure (triggers rollback)

### 4. **Validation**
Validate both preconditions and postconditions:

```python
# Preconditions: Can migration proceed?
def validate_preconditions() -> bool:
    # Check version, files, permissions, disk space
    pass

# Postconditions: Did migration succeed?
def validate_postconditions() -> bool:
    # Check files created/moved, config valid, data intact
    pass
```

### 5. **Atomic Operations**
Make operations atomic when possible:

```python
# Create temp location first, then move into place
temp_path = Path(dst).with_suffix(".tmp")
# ... write to temp_path ...
shutil.move(str(temp_path), str(dst))
```

## Troubleshooting

### Issue: Migration hangs or times out

**Cause:** Long-running file operations or network calls

**Solution:**
- Add timeout handling
- Break large operations into smaller chunks
- Log progress frequently

### Issue: Partial migration after failure

**Cause:** Some operations completed before failure

**Solution:**
- Automatic rollback handles this
- Ensure each operation is idempotent
- Test error scenarios

### Issue: Configuration not updated

**Cause:** JSON parsing errors or file permissions

**Solution:**
- Validate JSON before writing
- Check file permissions
- Log raw config before/after

## Related Documentation

- [Backup Management Guide](backup-management.md)
- [Upgrade Troubleshooting Guide](upgrade-troubleshooting.md)
- [STORY-078: Upgrade Mode with Migration Scripts](../../.ai_docs/Stories/STORY-078-upgrade-mode-migration-scripts.story.md)
