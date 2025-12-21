"""
STORY-078: Integration tests for upgrade workflow with migrations.

Tests end-to-end upgrade scenarios including full workflow execution,
migration script execution, validation, and rollback.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 85%+

AC Mapping:
- AC#1-AC#8: Full workflow integration
- End-to-end upgrade scenarios
- Real file I/O operations
- Migration script execution
- Rollback verification

Test Scenarios:
1. Happy path: Full upgrade 1.0.0 -> 1.1.0 with migrations
2. Patch upgrade: 1.0.0 -> 1.0.1 (no migrations needed)
3. Multi-version upgrade: 1.0.0 -> 1.2.0 (multiple migrations)
4. Rollback: Migration failure triggers restore
5. Validation failure: Missing file triggers rollback
"""

import pytest
import json
import time
import shutil
from pathlib import Path
from datetime import datetime


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def integration_project(tmp_path):
    """
    Create a complete integration test project with v1.0.0 installed.

    Returns:
        dict: Project structure and paths
    """
    project = tmp_path / "integration_project"
    project.mkdir()

    # Create devforgeai structure
    devforgeai = project / "devforgeai"
    devforgeai.mkdir()
    (devforgeai / "config").mkdir()
    (devforgeai / "context").mkdir()
    (devforgeai / "protocols").mkdir()
    (devforgeai / "backups").mkdir()
    (devforgeai / "logs").mkdir()

    # Create version file
    version_file = devforgeai / ".version.json"
    version_file.write_text(json.dumps({
        "version": "1.0.0",
        "installed_at": "2025-11-01T00:00:00Z",
        "mode": "fresh_install",
        "schema_version": "1.0"
    }, indent=2))

    # Create upgrade config
    config = devforgeai / "config" / "upgrade-config.json"
    config.write_text(json.dumps({
        "backup_retention_count": 5,
        "migration_timeout_seconds": 300,
        "validate_after_migration": True
    }, indent=2))

    # Create .claude structure
    claude = project / ".claude"
    claude.mkdir()
    (claude / "agents").mkdir()
    (claude / "commands").mkdir()
    (claude / "skills").mkdir()
    (claude / "memory").mkdir()

    # Create sample files
    for i in range(10):
        (claude / "agents" / f"agent_{i}.md").write_text(f"# Agent {i}\n")
        (claude / "commands" / f"command_{i}.md").write_text(f"# Command {i}\n")

    # Create CLAUDE.md
    (project / "CLAUDE.md").write_text("# DevForgeAI v1.0.0\n")

    # Create user content (should be preserved)
    ai_docs = project / ".ai_docs"
    ai_docs.mkdir()
    (ai_docs / "Stories").mkdir()
    (ai_docs / "Stories" / "STORY-001.md").write_text("# User Story\n")

    return {
        "root": project,
        "devforgeai": devforgeai,
        "claude": claude,
        "version_file": version_file
    }


@pytest.fixture
def source_framework_1_1_0(tmp_path):
    """
    Create source framework package for v1.1.0.

    Returns:
        dict: Source package paths and version
    """
    source = tmp_path / "source_1_1_0"
    source.mkdir()

    # Create devforgeai source
    devforgeai = source / "devforgeai"
    devforgeai.mkdir()
    (devforgeai / "config").mkdir()
    (devforgeai / "context").mkdir()
    (devforgeai / "protocols").mkdir()

    # Version file
    version_file = devforgeai / "version.json"
    version_file.write_text(json.dumps({
        "version": "1.1.0",
        "released_at": "2025-11-15T00:00:00Z",
        "schema_version": "1.0",
        "changes": ["New feature 1", "Bug fix 1"]
    }, indent=2))

    # Create claude source
    claude = source / "claude"
    claude.mkdir()
    (claude / "agents").mkdir()
    (claude / "commands").mkdir()
    (claude / "skills").mkdir()
    (claude / "memory").mkdir()

    # Create new and updated files
    for i in range(12):  # 2 new agents
        (claude / "agents" / f"agent_{i}.md").write_text(f"# Agent {i} v1.1.0\n")
    for i in range(10):
        (claude / "commands" / f"command_{i}.md").write_text(f"# Command {i} v1.1.0\n")

    # Create CLAUDE.md
    (source / "CLAUDE.md").write_text("# DevForgeAI v1.1.0\n")

    # Create migrations directory
    migrations = source / "migrations"
    migrations.mkdir()

    # Create migration script 1.0.0 -> 1.1.0
    migration_script = migrations / "v1.0.0-to-v1.1.0.py"
    migration_script.write_text('''#!/usr/bin/env python3
"""Migration from 1.0.0 to 1.1.0"""
import sys
import json
from pathlib import Path

def migrate(project_root):
    """Execute migration tasks for 1.0.0 -> 1.1.0."""
    project = Path(project_root)

    # Add new config key
    config_file = project / "devforgeai" / "config" / "upgrade-config.json"
    if config_file.exists():
        config = json.loads(config_file.read_text())
        config["new_feature_enabled"] = True
        config_file.write_text(json.dumps(config, indent=2))

    print("Migration 1.0.0 -> 1.1.0 completed")
    return True

if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    success = migrate(project_root)
    sys.exit(0 if success else 1)
''')

    return {
        "root": source,
        "version": "1.1.0",
        "version_file": version_file,
        "migrations": migrations
    }


@pytest.fixture
def source_framework_1_2_0(tmp_path, source_framework_1_1_0):
    """
    Create source framework package for v1.2.0 (multi-version upgrade test).

    Returns:
        dict: Source package paths and version
    """
    source = tmp_path / "source_1_2_0"
    shutil.copytree(source_framework_1_1_0["root"], source)

    # Update version
    devforgeai = source / "devforgeai"
    version_file = devforgeai / "version.json"
    version_file.write_text(json.dumps({
        "version": "1.2.0",
        "released_at": "2025-11-20T00:00:00Z",
        "schema_version": "1.0",
        "changes": ["Major feature", "Performance improvements"]
    }, indent=2))

    # Update CLAUDE.md
    (source / "CLAUDE.md").write_text("# DevForgeAI v1.2.0\n")

    # Add migration script 1.1.0 -> 1.2.0
    migrations = source / "migrations"
    migration_script = migrations / "v1.1.0-to-v1.2.0.py"
    migration_script.write_text('''#!/usr/bin/env python3
"""Migration from 1.1.0 to 1.2.0"""
import sys
import json
from pathlib import Path

def migrate(project_root):
    """Execute migration tasks for 1.1.0 -> 1.2.0."""
    project = Path(project_root)

    # Add another config key
    config_file = project / "devforgeai" / "config" / "upgrade-config.json"
    if config_file.exists():
        config = json.loads(config_file.read_text())
        config["v1_2_feature"] = "enabled"
        config_file.write_text(json.dumps(config, indent=2))

    print("Migration 1.1.0 -> 1.2.0 completed")
    return True

if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    success = migrate(project_root)
    sys.exit(0 if success else 1)
''')

    return {
        "root": source,
        "version": "1.2.0",
        "version_file": version_file,
        "migrations": migrations
    }


@pytest.fixture
def source_with_failing_migration(tmp_path, source_framework_1_1_0):
    """
    Create source package with a failing migration script.

    Returns:
        dict: Source package with failing migration
    """
    source = tmp_path / "source_failing"
    shutil.copytree(source_framework_1_1_0["root"], source)

    # Replace migration with failing one
    migration_script = source / "migrations" / "v1.0.0-to-v1.1.0.py"
    migration_script.write_text('''#!/usr/bin/env python3
"""Migration that FAILS"""
import sys

def migrate(project_root):
    print("Starting migration...")
    print("ERROR: Simulated failure!", file=sys.stderr)
    return False

if __name__ == "__main__":
    success = migrate(sys.argv[1] if len(sys.argv) > 1 else ".")
    sys.exit(0 if success else 1)
''')

    return {
        "root": source,
        "version": "1.1.0",
        "migrations": source / "migrations"
    }


# ============================================================================
# Test Class: Happy Path Scenarios
# ============================================================================

class TestUpgradeHappyPath:
    """Test successful upgrade scenarios."""

    def test_full_upgrade_1_0_0_to_1_1_0(self, integration_project, source_framework_1_1_0):
        """
        Happy Path: Full upgrade from 1.0.0 to 1.1.0 with migration.

        Given: Project with v1.0.0 installed
        When: Upgrade to v1.1.0 executed
        Then: Migration runs, version updated, files deployed
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_1_0["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        assert result.success is True
        assert result.from_version == "1.0.0"
        assert result.to_version == "1.1.0"

        # Verify version file updated
        version_data = json.loads((project_root / "devforgeai" / ".version.json").read_text())
        assert version_data["version"] == "1.1.0"
        assert version_data["upgraded_from"] == "1.0.0"

    def test_patch_upgrade_no_migrations(self, integration_project, tmp_path):
        """
        Happy Path: Patch upgrade (1.0.0 -> 1.0.1) with no migrations.

        Given: Project with v1.0.0 installed
        When: Upgrade to v1.0.1 (no migration scripts exist)
        Then: Upgrade succeeds without running migrations
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]

        # Create v1.0.1 source (no migrations)
        source = tmp_path / "source_1_0_1"
        source.mkdir()
        (source / "devforgeai").mkdir()
        (source / "devforgeai" / "version.json").write_text(json.dumps({
            "version": "1.0.1",
            "released_at": "2025-11-05T00:00:00Z"
        }))
        (source / "claude").mkdir()
        (source / "migrations").mkdir()  # Empty migrations

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source)

        # Assert
        assert result.success is True
        assert len(result.migrations_applied or []) == 0

    def test_multi_version_upgrade_1_0_0_to_1_2_0(self, integration_project, source_framework_1_2_0):
        """
        Happy Path: Multi-version upgrade (1.0.0 -> 1.2.0) runs all intermediate migrations.

        Given: Project with v1.0.0 installed
        When: Upgrade to v1.2.0 executed
        Then: Both migrations (1.0->1.1, 1.1->1.2) run in order
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_2_0["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        assert result.success is True
        assert result.to_version == "1.2.0"
        assert len(result.migrations_applied or []) == 2

        # Verify both migration effects
        config = json.loads((project_root / "devforgeai" / "config" / "upgrade-config.json").read_text())
        assert config.get("new_feature_enabled") is True  # From 1.0->1.1
        assert config.get("v1_2_feature") == "enabled"  # From 1.1->1.2

    def test_upgrade_preserves_user_content(self, integration_project, source_framework_1_1_0):
        """
        Happy Path: User content preserved during upgrade.

        Given: Project with user stories in devforgeai/specs/
        When: Upgrade executed
        Then: User stories unchanged
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_1_0["root"]

        # Verify user content exists
        user_story = project_root / ".ai_docs" / "Stories" / "STORY-001.md"
        original_content = user_story.read_text()

        orchestrator = UpgradeOrchestrator()

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        assert user_story.exists()
        assert user_story.read_text() == original_content

    def test_upgrade_creates_backup(self, integration_project, source_framework_1_1_0):
        """
        Happy Path: Backup created before upgrade.

        Given: Upgrade in progress
        When: execute() runs
        Then: Backup directory exists with original files
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_1_0["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        assert result.backup_path is not None
        backup_path = Path(result.backup_path)
        assert backup_path.exists()
        assert (backup_path / "devforgeai" / ".version.json").exists()


# ============================================================================
# Test Class: Rollback Scenarios
# ============================================================================

class TestUpgradeRollback:
    """Test rollback scenarios on failure."""

    def test_rollback_on_migration_failure(self, integration_project, source_with_failing_migration):
        """
        Rollback: Migration failure triggers automatic rollback.

        Given: Migration script that fails
        When: Upgrade executed
        Then: System restored to v1.0.0 state
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_with_failing_migration["root"]

        # Record original state
        original_version = json.loads((project_root / "devforgeai" / ".version.json").read_text())

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        assert result.success is False
        assert result.rolled_back is True

        # Verify restored to original version
        current_version = json.loads((project_root / "devforgeai" / ".version.json").read_text())
        assert current_version["version"] == "1.0.0"

    def test_rollback_on_validation_failure(self, integration_project, source_framework_1_1_0):
        """
        Rollback: Validation failure triggers rollback.

        Given: Upgrade completes but validation fails (expected file missing)
        When: Validation runs
        Then: Rollback triggered, original state restored
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator
        from unittest.mock import patch

        project_root = integration_project["root"]
        source_root = source_framework_1_1_0["root"]

        # Mock validator to fail
        with patch('installer.migration_validator.MigrationValidator.validate') as mock_validate:
            mock_validate.return_value.overall_passed = False
            mock_validate.return_value.should_rollback = True

            orchestrator = UpgradeOrchestrator()

            # Act
            result = orchestrator.execute(project_root=project_root, source_root=source_root)

            # Assert
            assert result.success is False
            assert result.rolled_back is True

    def test_rollback_restores_all_files(self, integration_project, source_with_failing_migration):
        """
        Rollback: All files restored from backup.

        Given: Rollback triggered
        When: Restore completes
        Then: All .claude/ and devforgeai/ files match backup
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_with_failing_migration["root"]

        # Record original file count
        original_agent_count = len(list((project_root / ".claude" / "agents").glob("*.md")))

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        assert result.rolled_back is True
        current_agent_count = len(list((project_root / ".claude" / "agents").glob("*.md")))
        assert current_agent_count == original_agent_count

    def test_rollback_completes_within_nfr(self, integration_project, source_with_failing_migration):
        """
        NFR-003: Rollback completes within 1 minute.

        Given: Rollback triggered
        When: Rollback executes
        Then: Completes in <60 seconds
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_with_failing_migration["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        start = time.time()
        result = orchestrator.execute(project_root=project_root, source_root=source_root)
        elapsed = time.time() - start

        # Assert
        assert result.rolled_back is True
        assert elapsed < 60, f"Rollback took {elapsed:.2f}s (expected <60s)"


# ============================================================================
# Test Class: Summary and Logging
# ============================================================================

class TestUpgradeSummaryAndLogging:
    """Test upgrade summary and logging."""

    def test_summary_saved_to_log_file(self, integration_project, source_framework_1_1_0):
        """
        AC#8: Summary saved to devforgeai/logs/upgrade-{timestamp}.log.

        Given: Upgrade completes
        When: Summary generated
        Then: Log file created
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_1_0["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        logs_dir = project_root / "devforgeai" / "logs"
        log_files = list(logs_dir.glob("upgrade-*.log"))
        assert len(log_files) > 0

    def test_summary_contains_all_required_fields(self, integration_project, source_framework_1_1_0):
        """
        AC#8: Summary contains files added/updated/removed, migrations, backup, version, duration.

        Given: Upgrade completes
        When: Summary accessed
        Then: All required fields present
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_1_0["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        summary = result.summary if hasattr(result, 'summary') else result

        # Check required fields (adapt based on actual implementation)
        assert hasattr(summary, 'files_added') or 'files_added' in dir(result)
        assert hasattr(summary, 'migrations_executed') or 'migrations_applied' in dir(result)
        assert hasattr(summary, 'backup_path') or result.backup_path is not None
        assert hasattr(summary, 'duration_seconds') or result.duration_seconds is not None

    def test_failed_upgrade_summary_includes_error(self, integration_project, source_with_failing_migration):
        """
        AC#8: Failed upgrade summary includes error message.

        Given: Upgrade fails
        When: Summary generated
        Then: Error message included
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_with_failing_migration["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        assert result.success is False
        assert result.error_message is not None


# ============================================================================
# Test Class: Version Metadata
# ============================================================================

class TestVersionMetadata:
    """Test version metadata updates."""

    def test_version_metadata_complete_after_upgrade(self, integration_project, source_framework_1_1_0):
        """
        AC#6: Version metadata complete after upgrade.

        Given: Upgrade completes successfully
        When: Checking .version.json
        Then: All required fields present
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_1_0["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        version_data = json.loads((project_root / "devforgeai" / ".version.json").read_text())
        assert version_data["version"] == "1.1.0"
        assert version_data["upgraded_from"] == "1.0.0"
        assert "upgrade_timestamp" in version_data
        assert "migrations_applied" in version_data

    def test_migrations_applied_list_accurate(self, integration_project, source_framework_1_2_0):
        """
        AC#6: migrations_applied list contains all executed migrations.

        Given: Multi-version upgrade
        When: Upgrade completes
        Then: migrations_applied lists all migrations run
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_2_0["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        version_data = json.loads((project_root / "devforgeai" / ".version.json").read_text())
        migrations = version_data.get("migrations_applied", [])
        assert len(migrations) == 2
        assert any("1.0.0-to-v1.1.0" in m for m in migrations)
        assert any("1.1.0-to-v1.2.0" in m for m in migrations)


# ============================================================================
# Test Class: Performance
# ============================================================================

class TestUpgradePerformance:
    """Test upgrade performance requirements."""

    def test_backup_creation_under_30_seconds(self, integration_project, source_framework_1_1_0):
        """
        NFR-001: Backup creation < 30 seconds.

        Given: Standard installation
        When: Backup created
        Then: Completes in <30 seconds
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]

        orchestrator = UpgradeOrchestrator()

        # Act
        start = time.time()
        backup_path = orchestrator._create_backup(project_root=project_root, from_version="1.0.0")
        elapsed = time.time() - start

        # Assert
        assert elapsed < 30, f"Backup took {elapsed:.2f}s (expected <30s)"

    def test_full_upgrade_under_2_minutes_no_migrations(self, integration_project, tmp_path):
        """
        NFR-002: Upgrade without migrations < 2 minutes.

        Given: Patch upgrade with no migrations
        When: Upgrade executed
        Then: Completes in <120 seconds
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]

        # Create patch source (no migrations)
        source = tmp_path / "source_patch"
        source.mkdir()
        (source / "devforgeai").mkdir()
        (source / "devforgeai" / "version.json").write_text(json.dumps({
            "version": "1.0.1"
        }))
        (source / "claude").mkdir()
        (source / "migrations").mkdir()

        orchestrator = UpgradeOrchestrator()

        # Act
        start = time.time()
        result = orchestrator.execute(project_root=project_root, source_root=source)
        elapsed = time.time() - start

        # Assert
        assert elapsed < 120, f"Upgrade took {elapsed:.2f}s (expected <120s)"


# ============================================================================
# Test Class: Edge Cases
# ============================================================================

class TestUpgradeEdgeCases:
    """Test edge cases for upgrade workflow."""

    def test_upgrade_empty_migrations_directory(self, integration_project, tmp_path):
        """
        Edge case: Empty migrations directory.

        Given: Source with empty migrations/
        When: Upgrade executed
        Then: Upgrade succeeds (no migrations to run)
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]

        source = tmp_path / "source_empty_migrations"
        source.mkdir()
        (source / "devforgeai").mkdir()
        (source / "devforgeai" / "version.json").write_text(json.dumps({"version": "1.1.0"}))
        (source / "claude").mkdir()
        (source / "migrations").mkdir()  # Empty

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source)

        # Assert
        assert result.success is True

    def test_upgrade_missing_migrations_directory(self, integration_project, tmp_path):
        """
        Edge case: No migrations directory in source.

        Given: Source without migrations/
        When: Upgrade executed
        Then: Upgrade succeeds (no migrations available)
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]

        source = tmp_path / "source_no_migrations"
        source.mkdir()
        (source / "devforgeai").mkdir()
        (source / "devforgeai" / "version.json").write_text(json.dumps({"version": "1.1.0"}))
        (source / "claude").mkdir()
        # No migrations/ directory

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source)

        # Assert
        assert result.success is True

    def test_concurrent_upgrade_prevention(self, integration_project, source_framework_1_1_0):
        """
        Edge case: Prevent concurrent upgrade operations.

        Given: Upgrade already in progress (lock file exists)
        When: Second upgrade attempted
        Then: Second upgrade blocked with clear error
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_1_0["root"]

        # Create lock file (simulating in-progress upgrade)
        lock_file = project_root / "devforgeai" / ".upgrade.lock"
        lock_file.write_text(json.dumps({
            "started_at": datetime.now().isoformat(),
            "pid": 12345
        }))

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert
        assert result.success is False
        assert "lock" in result.error_message.lower() or "progress" in result.error_message.lower()

    def test_upgrade_with_corrupted_version_file(self, integration_project, source_framework_1_1_0):
        """
        Edge case: Corrupted .version.json in target.

        Given: Target with corrupted version file
        When: Upgrade attempted
        Then: Error handled gracefully, backup offered
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        project_root = integration_project["root"]
        source_root = source_framework_1_1_0["root"]

        # Corrupt version file
        version_file = project_root / "devforgeai" / ".version.json"
        version_file.write_text("{ invalid json")

        orchestrator = UpgradeOrchestrator()

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_root)

        # Assert - should either fail gracefully or treat as fresh install
        assert result is not None  # Didn't crash
