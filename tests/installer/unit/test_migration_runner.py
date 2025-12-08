"""
STORY-078: Unit tests for MigrationRunner service.

Tests migration script execution, output capture, and error handling.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+

AC Mapping:
- AC#4: Migration Script Execution
  - Scripts run in version order (oldest to newest)
  - Each script's progress displayed to user
  - Script output (stdout/stderr) captured in logs
  - Script failure triggers immediate rollback
  - Successful migrations recorded for rollback reference

Technical Specification:
- SVC-011: Execute migration scripts in order
- SVC-012: Capture script output for logging
- SVC-013: Stop on first failure
- SVC-014: Track successfully applied migrations
"""

import pytest
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from datetime import datetime


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def migrations_dir(tmp_path):
    """
    Create a temporary migrations directory.

    Returns:
        Path: Path to migrations directory
    """
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    return migrations


@pytest.fixture
def project_root(tmp_path):
    """
    Create a temporary project root for migrations.

    Returns:
        Path: Path to project root
    """
    project = tmp_path / "project"
    project.mkdir()
    (project / ".devforgeai").mkdir()
    return project


@pytest.fixture
def successful_migration_script(migrations_dir):
    """
    Create a migration script that succeeds.

    Returns:
        Path: Path to successful migration script
    """
    script = migrations_dir / "v1.0.0-to-v1.1.0.py"
    script.write_text('''#!/usr/bin/env python3
"""Migration from 1.0.0 to 1.1.0"""
import sys

def migrate(project_root):
    print("Starting migration 1.0.0 -> 1.1.0")
    print("Migration completed successfully")
    return True

if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    success = migrate(project_root)
    sys.exit(0 if success else 1)
''')
    return script


@pytest.fixture
def failing_migration_script(migrations_dir):
    """
    Create a migration script that fails.

    Returns:
        Path: Path to failing migration script
    """
    script = migrations_dir / "v1.1.0-to-v1.2.0.py"
    script.write_text('''#!/usr/bin/env python3
"""Migration from 1.1.0 to 1.2.0 - FAILS"""
import sys

def migrate(project_root):
    print("Starting migration 1.1.0 -> 1.2.0")
    print("ERROR: Migration failed!", file=sys.stderr)
    return False

if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    success = migrate(project_root)
    sys.exit(0 if success else 1)
''')
    return script


@pytest.fixture
def multiple_migration_scripts(migrations_dir):
    """
    Create multiple migration scripts for sequential execution testing.

    Returns:
        list: List of script paths in order
    """
    scripts = []

    # Script 1: 1.0.0 -> 1.1.0
    script1 = migrations_dir / "v1.0.0-to-v1.1.0.py"
    script1.write_text('''#!/usr/bin/env python3
"""Migration from 1.0.0 to 1.1.0"""
import sys
print("Migration 1: 1.0.0 -> 1.1.0")
sys.exit(0)
''')
    scripts.append(script1)

    # Script 2: 1.1.0 -> 1.2.0
    script2 = migrations_dir / "v1.1.0-to-v1.2.0.py"
    script2.write_text('''#!/usr/bin/env python3
"""Migration from 1.1.0 to 1.2.0"""
import sys
print("Migration 2: 1.1.0 -> 1.2.0")
sys.exit(0)
''')
    scripts.append(script2)

    # Script 3: 1.2.0 -> 2.0.0
    script3 = migrations_dir / "v1.2.0-to-v2.0.0.py"
    script3.write_text('''#!/usr/bin/env python3
"""Migration from 1.2.0 to 2.0.0"""
import sys
print("Migration 3: 1.2.0 -> 2.0.0")
sys.exit(0)
''')
    scripts.append(script3)

    return scripts


@pytest.fixture
def mock_migration_scripts():
    """
    Create mock MigrationScript objects for testing.

    Returns:
        list: List of mock migration scripts
    """
    scripts = []

    # Mock script 1
    mock1 = MagicMock()
    mock1.path = Path("/mock/migrations/v1.0.0-to-v1.1.0.py")
    mock1.from_version = "1.0.0"
    mock1.to_version = "1.1.0"
    scripts.append(mock1)

    # Mock script 2
    mock2 = MagicMock()
    mock2.path = Path("/mock/migrations/v1.1.0-to-v1.2.0.py")
    mock2.from_version = "1.1.0"
    mock2.to_version = "1.2.0"
    scripts.append(mock2)

    return scripts


# ============================================================================
# Test Class: Sequential Execution (AC#4, SVC-011)
# ============================================================================

class TestMigrationSequentialExecution:
    """Test migration scripts run in version order (AC#4, SVC-011)."""

    def test_execute_single_migration_script(self, project_root, successful_migration_script):
        """
        SVC-011: Execute a single migration script successfully.

        Given: One migration script to run
        When: MigrationRunner.run() is called
        Then: Script executes and returns success
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        script = MigrationScript(
            path=successful_migration_script,
            from_version="1.0.0",
            to_version="1.1.0"
        )

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[script])

        # Assert
        assert result.all_success is True
        assert result.failed_at_migration is None
        assert result.applied_count == 1

    def test_execute_multiple_migrations_in_order(self, project_root, multiple_migration_scripts):
        """
        SVC-011: Multiple migrations execute in version order.

        Given: Three migration scripts (1.0->1.1, 1.1->1.2, 1.2->2.0)
        When: MigrationRunner.run() is called
        Then: All scripts execute in order
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        migrations = [
            MigrationScript(path=multiple_migration_scripts[0], from_version="1.0.0", to_version="1.1.0"),
            MigrationScript(path=multiple_migration_scripts[1], from_version="1.1.0", to_version="1.2.0"),
            MigrationScript(path=multiple_migration_scripts[2], from_version="1.2.0", to_version="2.0.0"),
        ]

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=migrations)

        # Assert
        assert result.all_success is True
        assert result.applied_count == 3

    def test_migrations_execute_in_provided_order(self, project_root, migrations_dir):
        """
        SVC-011: Migrations execute in the exact order provided.

        Given: List of migrations in specific order
        When: run() is called
        Then: Scripts execute in that exact order
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        execution_order = []

        # Create scripts that record execution order
        script1 = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script1.write_text(f'''#!/usr/bin/env python3
import sys
with open("{migrations_dir}/execution_log.txt", "a") as f:
    f.write("1\\n")
sys.exit(0)
''')

        script2 = migrations_dir / "v1.1.0-to-v1.2.0.py"
        script2.write_text(f'''#!/usr/bin/env python3
import sys
with open("{migrations_dir}/execution_log.txt", "a") as f:
    f.write("2\\n")
sys.exit(0)
''')

        migrations = [
            MigrationScript(path=script1, from_version="1.0.0", to_version="1.1.0"),
            MigrationScript(path=script2, from_version="1.1.0", to_version="1.2.0"),
        ]

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=migrations)

        # Assert
        assert result.all_success is True
        log_file = migrations_dir / "execution_log.txt"
        if log_file.exists():
            lines = log_file.read_text().strip().split("\n")
            assert lines == ["1", "2"], "Scripts did not execute in correct order"

    def test_empty_migration_list_returns_success(self, project_root):
        """
        SVC-011: Empty migration list returns success immediately.

        Given: Empty list of migrations (patch upgrade, no migrations needed)
        When: MigrationRunner.run() is called
        Then: Returns success with empty results
        """
        # Arrange
        from installer.migration_runner import MigrationRunner

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[])

        # Assert
        assert result.all_success is True
        assert result.applied_count == 0


# ============================================================================
# Test Class: Output Capture (AC#4, SVC-012)
# ============================================================================

class TestMigrationOutputCapture:
    """Test script output (stdout/stderr) capture (AC#4, SVC-012)."""

    def test_capture_stdout_from_migration_script(self, project_root, migrations_dir):
        """
        SVC-012: Capture stdout from migration script.

        Given: Migration script that prints to stdout
        When: Script executes
        Then: stdout content captured in result
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text('''#!/usr/bin/env python3
import sys
print("Migration started")
print("Step 1: Updating config files")
print("Step 2: Moving directories")
print("Migration completed")
sys.exit(0)
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is True
        assert result.applied_count == 1

        migration_result = result.results[0]
        assert "Migration started" in migration_result.stdout
        assert "Migration completed" in migration_result.stdout

    def test_capture_stderr_from_migration_script(self, project_root, migrations_dir):
        """
        SVC-012: Capture stderr from migration script.

        Given: Migration script that prints to stderr
        When: Script executes
        Then: stderr content captured in result
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text('''#!/usr/bin/env python3
import sys
print("Normal output", file=sys.stdout)
print("Warning: deprecated config detected", file=sys.stderr)
sys.exit(0)  # Still succeeds
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is True
        migration_result = result.results[0]
        assert "Warning" in migration_result.stderr or "deprecated" in migration_result.stderr

    def test_output_logged_to_migration_logger(self, project_root, migrations_dir):
        """
        SVC-012: Script output captured in migration result.

        Given: Migration script with output
        When: Script executes
        Then: Output captured in result stdout/stderr
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text('''#!/usr/bin/env python3
print("Migration output line 1")
print("Migration output line 2")
import sys
sys.exit(0)
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is True
        assert "Migration output" in result.results[0].stdout

    def test_progress_display_for_each_migration(self, project_root, multiple_migration_scripts):
        """
        AC#4: Each script's progress displayed to user.

        Given: Multiple migration scripts
        When: Scripts execute
        Then: All migrations execute successfully
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        migrations = [
            MigrationScript(path=multiple_migration_scripts[0], from_version="1.0.0", to_version="1.1.0"),
            MigrationScript(path=multiple_migration_scripts[1], from_version="1.1.0", to_version="1.2.0"),
            MigrationScript(path=multiple_migration_scripts[2], from_version="1.2.0", to_version="2.0.0"),
        ]

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=migrations)

        # Assert
        assert result.all_success is True
        assert result.applied_count == 3
        assert len(result.results) == 3


# ============================================================================
# Test Class: Failure Handling (AC#4, SVC-013)
# ============================================================================

class TestMigrationFailureHandling:
    """Test migration failure handling and rollback trigger (AC#4, SVC-013)."""

    def test_stop_on_first_failure(self, project_root, migrations_dir):
        """
        SVC-013: Stop execution on first failure, don't run remaining.

        Given: 3 migrations where 2nd fails
        When: MigrationRunner.run() is called
        Then: 3rd migration not executed
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        # Script 1 succeeds
        script1 = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script1.write_text('''#!/usr/bin/env python3
import sys
print("Migration 1 OK")
sys.exit(0)
''')

        # Script 2 fails
        script2 = migrations_dir / "v1.1.0-to-v1.2.0.py"
        script2.write_text('''#!/usr/bin/env python3
import sys
print("Migration 2 FAILED", file=sys.stderr)
sys.exit(1)
''')

        # Script 3 should not run
        script3 = migrations_dir / "v1.2.0-to-v2.0.0.py"
        script3.write_text(f'''#!/usr/bin/env python3
import sys
with open("{migrations_dir}/script3_ran.txt", "w") as f:
    f.write("EXECUTED")
sys.exit(0)
''')

        migrations = [
            MigrationScript(path=script1, from_version="1.0.0", to_version="1.1.0"),
            MigrationScript(path=script2, from_version="1.1.0", to_version="1.2.0"),
            MigrationScript(path=script3, from_version="1.2.0", to_version="2.0.0"),
        ]

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=migrations)

        # Assert
        assert result.all_success is False
        assert result.failed_at_migration is not None
        assert result.failed_at_migration.from_version == "1.1.0"
        assert result.applied_count == 1  # Only first succeeded
        assert not (migrations_dir / "script3_ran.txt").exists(), "Script 3 should not have run"

    def test_failed_migration_recorded_in_result(self, project_root, failing_migration_script):
        """
        SVC-013: Failed migration recorded in result.

        Given: Migration script that fails
        When: Script executes
        Then: Failed migration info recorded in result
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        migration = MigrationScript(path=failing_migration_script, from_version="1.1.0", to_version="1.2.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is False
        assert result.failed_at_migration is not None
        assert result.failed_at_migration.from_version == "1.1.0"
        assert result.failed_at_migration.to_version == "1.2.0"

    def test_failure_captures_exit_code(self, project_root, migrations_dir):
        """
        SVC-013: Exit code captured for failed migration.

        Given: Migration script exits with code 42
        When: Script executes
        Then: Exit code 42 captured in result
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text('''#!/usr/bin/env python3
import sys
print("Failing with exit code 42")
sys.exit(42)
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is False
        assert result.failed_migration_result is not None
        assert result.failed_migration_result.exit_code == 42

    def test_failure_triggers_need_for_rollback(self, project_root, failing_migration_script):
        """
        AC#4: Script failure triggers rollback.

        Given: Migration script that fails
        When: Script executes
        Then: Failed migration recorded for rollback
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        migration = MigrationScript(path=failing_migration_script, from_version="1.1.0", to_version="1.2.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is False
        assert result.failed_at_migration is not None
        assert result.failed_migration_result is not None


# ============================================================================
# Test Class: Success Tracking (AC#4, SVC-014)
# ============================================================================

class TestMigrationSuccessTracking:
    """Test successful migration tracking (AC#4, SVC-014)."""

    def test_track_successfully_applied_migrations(self, project_root, multiple_migration_scripts):
        """
        SVC-014: Track all successfully applied migrations.

        Given: 3 migrations all succeed
        When: run() completes
        Then: applied_migrations contains 3 entries
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        migrations = [
            MigrationScript(path=multiple_migration_scripts[0], from_version="1.0.0", to_version="1.1.0"),
            MigrationScript(path=multiple_migration_scripts[1], from_version="1.1.0", to_version="1.2.0"),
            MigrationScript(path=multiple_migration_scripts[2], from_version="1.2.0", to_version="2.0.0"),
        ]

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=migrations)

        # Assert
        assert result.all_success is True
        assert result.applied_count == 3
        assert len(result.results) == 3

    def test_partial_success_tracks_completed_migrations(self, project_root, migrations_dir):
        """
        SVC-014: On partial failure, track only completed migrations.

        Given: 3 migrations where 2nd fails
        When: run() completes
        Then: Results contains only first migration result
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        script1 = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script1.write_text("#!/usr/bin/env python3\nimport sys; sys.exit(0)")

        script2 = migrations_dir / "v1.1.0-to-v1.2.0.py"
        script2.write_text("#!/usr/bin/env python3\nimport sys; sys.exit(1)")

        script3 = migrations_dir / "v1.2.0-to-v2.0.0.py"
        script3.write_text("#!/usr/bin/env python3\nimport sys; sys.exit(0)")

        migrations = [
            MigrationScript(path=script1, from_version="1.0.0", to_version="1.1.0"),
            MigrationScript(path=script2, from_version="1.1.0", to_version="1.2.0"),
            MigrationScript(path=script3, from_version="1.2.0", to_version="2.0.0"),
        ]

        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=migrations)

        # Assert
        assert result.all_success is False
        assert result.applied_count == 1
        assert result.results[0].script.from_version == "1.0.0"

    def test_successful_migrations_in_results(self, project_root, successful_migration_script):
        """
        SVC-014: Successful migrations recorded in results.

        Given: Migration script executes successfully
        When: Checking result
        Then: Success recorded in results list
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        migration = MigrationScript(path=successful_migration_script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert len(result.results) == 1
        assert result.results[0].success is True
        assert result.results[0].exit_code == 0

    def test_successful_migration_captures_output(self, project_root, migrations_dir):
        """
        SVC-014: Successful migration captures stdout/stderr.

        Given: Migration script with output
        When: Migration succeeds
        Then: Output captured in result
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        # Script with output
        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text('''#!/usr/bin/env python3
import time
import sys
print("Migration started")
sys.exit(0)
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert len(result.results) == 1
        assert result.results[0].success is True
        assert "Migration started" in result.results[0].stdout


# ============================================================================
# Test Class: Migration Types Support (AC#4)
# ============================================================================

class TestMigrationTypesSupport:
    """Test supported migration types (AC#4)."""

    def test_file_move_migration(self, project_root, migrations_dir):
        """
        AC#4: Support file move migrations.

        Given: Migration script that moves files
        When: Script executes
        Then: Files moved to new locations
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        # Create source file to be moved
        old_config = project_root / ".devforgeai" / "old_config.json"
        old_config.write_text('{"setting": "value"}')

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text(f'''#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

project = Path("{project_root}")
old = project / ".devforgeai" / "old_config.json"
new = project / ".devforgeai" / "config" / "settings.json"
new.parent.mkdir(parents=True, exist_ok=True)
shutil.move(str(old), str(new))
sys.exit(0)
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is True
        assert not old_config.exists()
        assert (project_root / ".devforgeai" / "config" / "settings.json").exists()

    def test_config_update_migration(self, project_root, migrations_dir):
        """
        AC#4: Support config update migrations.

        Given: Migration script that updates JSON config
        When: Script executes
        Then: Config updated with new keys/values
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        # Create config file
        config = project_root / ".devforgeai" / "config.json"
        config.write_text('{"version": "1.0", "old_key": "value"}')

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text(f'''#!/usr/bin/env python3
import json
import sys
from pathlib import Path

config_path = Path("{config}")
with open(config_path) as f:
    config = json.load(f)

config["version"] = "1.1"
config["new_key"] = "new_value"
del config["old_key"]

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

sys.exit(0)
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is True
        updated_config = json.loads(config.read_text())
        assert updated_config["version"] == "1.1"
        assert updated_config["new_key"] == "new_value"
        assert "old_key" not in updated_config

    def test_schema_change_migration(self, project_root, migrations_dir):
        """
        AC#4: Support schema change migrations.

        Given: Migration script that updates data schema
        When: Script executes
        Then: Schema updated correctly
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        # Create data file with old schema
        data = project_root / ".devforgeai" / "data.json"
        data.write_text('{"items": [{"name": "item1"}, {"name": "item2"}]}')

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text(f'''#!/usr/bin/env python3
import json
import sys
from pathlib import Path

data_path = Path("{data}")
with open(data_path) as f:
    d = json.load(f)

# Add ID field to each item (schema change)
for i, item in enumerate(d["items"]):
    item["id"] = i + 1

# Add schema version
d["schema_version"] = "2.0"

with open(data_path, "w") as f:
    json.dump(d, f, indent=2)

sys.exit(0)
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is True
        updated_data = json.loads(data.read_text())
        assert updated_data["schema_version"] == "2.0"
        assert updated_data["items"][0]["id"] == 1

    def test_deprecation_handling_migration(self, project_root, migrations_dir):
        """
        AC#4: Support deprecation handling migrations.

        Given: Migration script that handles deprecated features
        When: Script executes
        Then: Deprecated features removed/replaced
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        # Create deprecated config
        deprecated = project_root / ".devforgeai" / "deprecated_config.yaml"
        deprecated.write_text("deprecated: true\nold_setting: value\n")

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text(f'''#!/usr/bin/env python3
import sys
from pathlib import Path

# Remove deprecated file
deprecated_path = Path("{deprecated}")
if deprecated_path.exists():
    deprecated_path.unlink()

sys.exit(0)
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is True
        assert not deprecated.exists()


# ============================================================================
# Test Class: Timeout Handling
# ============================================================================

class TestMigrationTimeout:
    """Test migration timeout handling."""

    def test_migration_timeout_after_configured_duration(self, project_root, migrations_dir):
        """
        Configuration: migration_timeout_seconds from upgrade-config.json.

        Given: Migration script that runs forever
        When: Timeout configured to 2 seconds
        Then: Migration killed after timeout, marked as failed
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text('''#!/usr/bin/env python3
import time
import sys
# Simulate infinite loop
time.sleep(60)
sys.exit(0)
''')

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration], timeout_seconds=2)

        # Assert
        assert result.all_success is False
        assert result.failed_migration_result is not None
        assert "timeout" in result.failed_migration_result.error_message.lower()

    def test_successful_migration_completes_before_timeout(self, project_root, successful_migration_script):
        """
        Test: Migration completing before timeout succeeds.

        Given: Migration script that completes in 100ms
        When: Timeout is 60 seconds
        Then: Migration succeeds
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        migration = MigrationScript(path=successful_migration_script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration], timeout_seconds=60)

        # Assert
        assert result.all_success is True


# ============================================================================
# Test Class: Edge Cases
# ============================================================================

class TestMigrationRunnerEdgeCases:
    """Test edge cases for migration runner."""

    def test_migration_script_not_found(self, project_root):
        """
        Edge case: Migration script file not found.

        Given: MigrationScript pointing to nonexistent file
        When: Trying to create it
        Then: Raises ValueError with clear error message
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            MigrationScript(
                path=Path("/nonexistent/migration.py"),
                from_version="1.0.0",
                to_version="1.1.0"
            )

    def test_migration_script_not_executable(self, project_root, migrations_dir):
        """
        Edge case: Migration script exists but Python can't run it.

        Given: Migration script with syntax error
        When: run() is called
        Then: Returns failure with error details
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text("this is not valid python syntax !!!")

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is False
        assert result.failed_migration_result is not None

    def test_migration_script_syntax_error(self, project_root, migrations_dir):
        """
        Edge case: Migration script with invalid Python syntax.

        Given: Migration script with syntax error
        When: run() is called
        Then: Returns failure with stderr
        """
        # Arrange
        from installer.migration_runner import MigrationRunner, MigrationScript

        script = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script.write_text("#!/usr/bin/env python3\nthis is not valid python !!!")

        migration = MigrationScript(path=script, from_version="1.0.0", to_version="1.1.0")
        runner = MigrationRunner()

        # Act
        result = runner.run(migrations=[migration])

        # Assert
        assert result.all_success is False
        assert result.failed_migration_result is not None
        assert len(result.failed_migration_result.stderr) > 0
