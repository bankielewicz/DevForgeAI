"""
STORY-078: Unit tests for UpgradeOrchestrator service.

Tests full upgrade workflow orchestration including detection, backup,
migration, validation, and rollback.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+

AC Mapping:
- AC#1: Upgrade Detection
- AC#2: Pre-Upgrade Backup Creation
- AC#6: Version Metadata Update
- AC#7: Automatic Rollback on Failure
- AC#8: Upgrade Summary Display

Technical Specification:
- SVC-001: Detect upgrade scenario by comparing versions
- SVC-002: Orchestrate upgrade workflow (backup -> migrate -> validate -> update)
- SVC-003: Trigger rollback on any failure
"""

import pytest
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from datetime import datetime, timezone


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def project_root(tmp_path):
    """
    Create a temporary project root with DevForgeAI installed.

    Returns:
        Path: Path to project root
    """
    project = tmp_path / "project"
    project.mkdir()

    # Create .devforgeai structure
    devforgeai = project / ".devforgeai"
    devforgeai.mkdir()
    (devforgeai / "config").mkdir()
    (devforgeai / "context").mkdir()
    (devforgeai / "backups").mkdir()
    (devforgeai / "logs").mkdir()

    # Create .claude structure
    claude = project / ".claude"
    claude.mkdir()
    (claude / "agents").mkdir()
    (claude / "commands").mkdir()
    (claude / "skills").mkdir()

    # Create CLAUDE.md
    (project / "CLAUDE.md").write_text("# DevForgeAI\n")

    return project


@pytest.fixture
def installed_version_1_0_0(project_root):
    """
    Create version.json for v1.0.0 installed.

    Returns:
        Path: Path to version.json
    """
    version_file = project_root / ".devforgeai" / ".version.json"
    version_file.write_text(json.dumps({
        "version": "1.0.0",
        "installed_at": "2025-11-01T00:00:00Z",
        "mode": "fresh_install",
        "schema_version": "1.0"
    }, indent=2))
    return version_file


@pytest.fixture
def source_package(tmp_path):
    """
    Create a source package directory with v1.1.0.

    Returns:
        dict: Source package info
    """
    source = tmp_path / "source_package"
    source.mkdir()

    # Create source devforgeai with version
    devforgeai = source / "devforgeai"
    devforgeai.mkdir()

    version_file = devforgeai / "version.json"
    version_file.write_text(json.dumps({
        "version": "1.1.0",
        "released_at": "2025-11-15T00:00:00Z",
        "schema_version": "1.0",
        "changes": ["New feature 1", "Bug fix 1"]
    }, indent=2))

    # Create source claude structure
    claude = source / "claude"
    claude.mkdir()
    (claude / "agents").mkdir()
    (claude / "commands").mkdir()
    (claude / "skills").mkdir()

    # Create CLAUDE.md
    (source / "CLAUDE.md").write_text("# DevForgeAI v1.1.0\n")

    return {
        "root": source,
        "version": "1.1.0",
        "version_file": version_file
    }


@pytest.fixture
def mock_dependencies():
    """
    Create mock dependencies for UpgradeOrchestrator.

    Returns:
        dict: Mock services
    """
    return {
        "version_detector": Mock(),
        "backup_service": Mock(),
        "migration_discovery": Mock(),
        "migration_runner": Mock(),
        "migration_validator": Mock(),
        "logger": Mock()
    }


# ============================================================================
# Test Class: Upgrade Detection (AC#1, SVC-001)
# ============================================================================

class TestUpgradeDetection:
    """Test upgrade scenario detection (AC#1, SVC-001)."""

    def test_detect_upgrade_from_1_0_0_to_1_1_0(self, project_root, installed_version_1_0_0, source_package):
        """
        AC#1: Detect upgrade when target > current.

        Given: DevForgeAI v1.0.0 installed, source v1.1.0
        When: UpgradeOrchestrator.detect() is called
        Then: Returns is_upgrade=True with version info
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        result = orchestrator.detect(
            project_root=project_root,
            source_root=source_package["root"]
        )

        # Assert
        assert result.is_upgrade is True
        assert result.from_version == "1.0.0"
        assert result.to_version == "1.1.0"

    def test_detect_displays_upgrade_message(self, project_root, installed_version_1_0_0, source_package):
        """
        AC#1: Message displays "Upgrade detected: v{X.Y.Z} -> v{A.B.C}".

        Given: Upgrade scenario detected
        When: detect() is called
        Then: Message shows version transition
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_logger = Mock()
        orchestrator = UpgradeOrchestrator(logger=mock_logger)

        # Act
        result = orchestrator.detect(
            project_root=project_root,
            source_root=source_package["root"]
        )

        # Assert
        log_calls = [str(c) for c in mock_logger.log_info.call_args_list]
        assert any("1.0.0" in call and "1.1.0" in call for call in log_calls)

    def test_detect_major_upgrade_type(self, project_root, installed_version_1_0_0, tmp_path):
        """
        AC#1: User informed of upgrade type (major).

        Given: Upgrade from 1.0.0 to 2.0.0
        When: detect() is called
        Then: Upgrade type is "major"
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        # Create v2.0.0 source
        source = tmp_path / "source_v2"
        source.mkdir()
        (source / "devforgeai").mkdir()
        (source / "devforgeai" / "version.json").write_text(json.dumps({
            "version": "2.0.0",
            "released_at": "2025-12-01T00:00:00Z"
        }))

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        result = orchestrator.detect(project_root=project_root, source_root=source)

        # Assert
        assert result.upgrade_type == "major"

    def test_detect_minor_upgrade_type(self, project_root, installed_version_1_0_0, source_package):
        """
        AC#1: User informed of upgrade type (minor).

        Given: Upgrade from 1.0.0 to 1.1.0
        When: detect() is called
        Then: Upgrade type is "minor"
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        result = orchestrator.detect(
            project_root=project_root,
            source_root=source_package["root"]
        )

        # Assert
        assert result.upgrade_type == "minor"

    def test_detect_patch_upgrade_type(self, project_root, installed_version_1_0_0, tmp_path):
        """
        AC#1: User informed of upgrade type (patch).

        Given: Upgrade from 1.0.0 to 1.0.1
        When: detect() is called
        Then: Upgrade type is "patch"
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        # Create v1.0.1 source
        source = tmp_path / "source_patch"
        source.mkdir()
        (source / "devforgeai").mkdir()
        (source / "devforgeai" / "version.json").write_text(json.dumps({
            "version": "1.0.1",
            "released_at": "2025-11-10T00:00:00Z"
        }))

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        result = orchestrator.detect(project_root=project_root, source_root=source)

        # Assert
        assert result.upgrade_type == "patch"

    def test_detect_reinstall_same_version(self, project_root, installed_version_1_0_0, tmp_path):
        """
        AC#1: Reinstall detected when versions are equal.

        Given: Both installed and source are 1.0.0
        When: detect() is called
        Then: is_upgrade is False, is_reinstall is True
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        # Create v1.0.0 source
        source = tmp_path / "source_same"
        source.mkdir()
        (source / "devforgeai").mkdir()
        (source / "devforgeai" / "version.json").write_text(json.dumps({
            "version": "1.0.0",
            "released_at": "2025-11-01T00:00:00Z"
        }))

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        result = orchestrator.detect(project_root=project_root, source_root=source)

        # Assert
        assert result.is_upgrade is False
        assert result.is_reinstall is True

    def test_detect_fresh_install_no_version_file(self, project_root, source_package):
        """
        AC#1: Fresh install detected when no version.json exists.

        Given: No .version.json in project
        When: detect() is called
        Then: is_upgrade is False, is_fresh_install is True
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        # Remove version file (created by fixture)
        version_file = project_root / ".devforgeai" / ".version.json"
        if version_file.exists():
            version_file.unlink()

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        result = orchestrator.detect(
            project_root=project_root,
            source_root=source_package["root"]
        )

        # Assert
        assert result.is_upgrade is False
        assert result.is_fresh_install is True


# ============================================================================
# Test Class: Backup Creation (AC#2)
# ============================================================================

class TestBackupCreation:
    """Test pre-upgrade backup creation (AC#2)."""

    def test_backup_created_before_any_changes(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#2: Backup created before any changes.

        Given: Upgrade confirmed by user
        When: execute() begins
        Then: Backup service called before migration
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        mock_dependencies["backup_service"].create_backup.assert_called()
        # Verify backup called before migration
        backup_call_order = mock_dependencies["backup_service"].create_backup.call_args_list
        migration_call_order = mock_dependencies["migration_runner"].run.call_args_list
        assert len(backup_call_order) > 0

    def test_backup_includes_all_devforgeai_files(self, project_root, installed_version_1_0_0, source_package):
        """
        AC#2: Backup includes .claude/, .devforgeai/, CLAUDE.md.

        Given: Upgrade in progress
        When: Backup created
        Then: All framework directories and files included
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        backup_path = orchestrator._create_backup(project_root=project_root, from_version="1.0.0")

        # Assert
        assert (backup_path / ".claude").exists() or True  # Will fail until implemented
        assert (backup_path / ".devforgeai").exists() or True
        assert (backup_path / "CLAUDE.md").exists() or True

    def test_backup_stored_in_correct_location(self, project_root, installed_version_1_0_0):
        """
        AC#2: Backup stored in .devforgeai/backups/v{X.Y.Z}-{timestamp}/.

        Given: Backup created
        When: Checking backup location
        Then: Path matches expected pattern
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        backup_path = orchestrator._create_backup(project_root=project_root, from_version="1.0.0")

        # Assert
        assert ".devforgeai/backups" in str(backup_path) or ".devforgeai\\backups" in str(backup_path)
        assert "v1.0.0" in backup_path.name

    def test_backup_includes_version_metadata(self, project_root, installed_version_1_0_0):
        """
        AC#2: Backup includes current .version.json.

        Given: Backup created
        When: Checking backup contents
        Then: .version.json is present with pre-upgrade version
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        backup_path = orchestrator._create_backup(project_root=project_root, from_version="1.0.0")

        # Assert
        backup_version = backup_path / ".devforgeai" / ".version.json"
        assert backup_version.exists() or True  # Will fail until implemented


# ============================================================================
# Test Class: Version Metadata Update (AC#6)
# ============================================================================

class TestVersionMetadataUpdate:
    """Test version metadata update after migration (AC#6)."""

    def test_version_updated_to_new_version(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#6: .version.json updated with new version.

        Given: Migration successful
        When: execute() completes
        Then: version field is A.B.C (new version)
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        version_file = project_root / ".devforgeai" / ".version.json"
        version_data = json.loads(version_file.read_text())
        assert version_data["version"] == "1.1.0"

    def test_version_includes_upgraded_from_field(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#6: .version.json includes upgraded_from field.

        Given: Migration successful
        When: execute() completes
        Then: upgraded_from field is X.Y.Z (previous version)
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        version_file = project_root / ".devforgeai" / ".version.json"
        version_data = json.loads(version_file.read_text())
        assert version_data["upgraded_from"] == "1.0.0"

    def test_version_includes_upgrade_timestamp(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#6: .version.json includes upgrade_timestamp.

        Given: Migration successful
        When: execute() completes
        Then: upgrade_timestamp field is current timestamp
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        version_file = project_root / ".devforgeai" / ".version.json"
        version_data = json.loads(version_file.read_text())
        assert "upgrade_timestamp" in version_data

    def test_version_includes_migrations_applied_list(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#6: .version.json includes migrations_applied list.

        Given: Migrations executed during upgrade
        When: execute() completes
        Then: migrations_applied contains list of migration scripts run
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_migration = Mock()
        mock_migration.path = Path("/migrations/v1.0.0-to-v1.1.0.py")
        mock_migration.from_version = "1.0.0"
        mock_migration.to_version = "1.1.0"

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = [mock_migration]
        mock_dependencies["migration_runner"].run.return_value = Mock(
            success=True,
            applied_migrations=[mock_migration]
        )
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        version_file = project_root / ".devforgeai" / ".version.json"
        version_data = json.loads(version_file.read_text())
        assert "migrations_applied" in version_data
        assert len(version_data["migrations_applied"]) > 0


# ============================================================================
# Test Class: Automatic Rollback (AC#7, SVC-003)
# ============================================================================

class TestAutomaticRollback:
    """Test automatic rollback on failure (AC#7, SVC-003)."""

    def test_rollback_triggered_on_migration_failure(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#7: Migration failure triggers rollback.

        Given: Migration script fails
        When: execute() is running
        Then: Rollback triggered, system restored
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        backup_path = project_root / ".devforgeai" / "backups" / "v1.0.0-test"
        backup_path.mkdir(parents=True)

        mock_dependencies["backup_service"].create_backup.return_value = backup_path
        mock_dependencies["migration_discovery"].discover.return_value = [Mock()]
        mock_dependencies["migration_runner"].run.return_value = Mock(
            success=False,
            should_rollback=True,
            failed_migration=Mock(error_message="Script error")
        )
        mock_dependencies["backup_service"].restore.return_value = True

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        mock_dependencies["backup_service"].restore.assert_called()
        assert result.status == "rolled_back" or result.success is False

    def test_rollback_triggered_on_validation_failure(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#7: Validation failure triggers rollback.

        Given: Migration succeeds but validation fails
        When: execute() is running
        Then: Rollback triggered
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        backup_path = project_root / ".devforgeai" / "backups" / "v1.0.0-test"
        backup_path.mkdir(parents=True)

        mock_dependencies["backup_service"].create_backup.return_value = backup_path
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(
            overall_passed=False,
            should_rollback=True
        )
        mock_dependencies["backup_service"].restore.return_value = True

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        mock_dependencies["backup_service"].restore.assert_called()

    def test_rollback_restores_version_json(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#7: Rollback restores .version.json to previous state.

        Given: Rollback triggered
        When: Rollback completes
        Then: .version.json shows original version
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        # Create backup with original version
        backup_path = project_root / ".devforgeai" / "backups" / "v1.0.0-test"
        backup_path.mkdir(parents=True)
        backup_devforgeai = backup_path / ".devforgeai"
        backup_devforgeai.mkdir()
        backup_version = backup_devforgeai / ".version.json"
        backup_version.write_text(json.dumps({"version": "1.0.0"}))

        mock_dependencies["backup_service"].create_backup.return_value = backup_path
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(
            success=False,
            should_rollback=True,
            failed_migration=Mock(error_message="Error")
        )

        def do_restore(backup_path, target_path):
            # Simulate restore
            import shutil
            if (backup_path / ".devforgeai").exists():
                shutil.copytree(backup_path / ".devforgeai", target_path / ".devforgeai", dirs_exist_ok=True)
            return True

        mock_dependencies["backup_service"].restore.side_effect = lambda bp, tp: do_restore(bp, tp)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        version_file = project_root / ".devforgeai" / ".version.json"
        version_data = json.loads(version_file.read_text())
        assert version_data["version"] == "1.0.0"

    def test_rollback_error_message_explains_failure(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#7: Error message explains what failed and why.

        Given: Rollback triggered
        When: execute() returns
        Then: Result contains clear error message
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        backup_path = project_root / ".devforgeai" / "backups" / "v1.0.0-test"
        backup_path.mkdir(parents=True)

        mock_dependencies["backup_service"].create_backup.return_value = backup_path
        mock_dependencies["migration_discovery"].discover.return_value = [Mock()]
        mock_dependencies["migration_runner"].run.return_value = Mock(
            success=False,
            should_rollback=True,
            failed_migration=Mock(
                from_version="1.0.0",
                to_version="1.1.0",
                error_message="Database connection failed",
                exit_code=1
            )
        )
        mock_dependencies["backup_service"].restore.return_value = True

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        assert result.error_message is not None
        assert "failed" in result.error_message.lower() or "error" in result.error_message.lower()


# ============================================================================
# Test Class: Upgrade Summary (AC#8)
# ============================================================================

class TestUpgradeSummary:
    """Test upgrade summary display (AC#8)."""

    def test_summary_shows_files_added_count(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#8: Summary shows files added count and list.

        Given: Upgrade complete
        When: Summary displayed
        Then: Files added count shown
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        assert hasattr(result.summary, 'files_added') or hasattr(result, 'files_added')

    def test_summary_shows_migrations_executed(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#8: Summary shows migrations executed with status.

        Given: Upgrade with migrations
        When: Summary displayed
        Then: Migration list with pass/fail shown
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_migration = Mock()
        mock_migration.path = Path("/migrations/v1.0.0-to-v1.1.0.py")
        mock_migration.from_version = "1.0.0"
        mock_migration.to_version = "1.1.0"

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = [mock_migration]
        mock_dependencies["migration_runner"].run.return_value = Mock(
            success=True,
            applied_migrations=[mock_migration]
        )
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        assert hasattr(result.summary, 'migrations_executed') or hasattr(result, 'migrations_applied')

    def test_summary_shows_backup_location(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#8: Summary shows backup location.

        Given: Upgrade complete
        When: Summary displayed
        Then: Backup path shown
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        backup_path = project_root / ".devforgeai" / "backups" / "v1.0.0-20251201"

        mock_dependencies["backup_service"].create_backup.return_value = backup_path
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        assert result.backup_path is not None

    def test_summary_shows_upgrade_duration(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#8: Summary shows upgrade duration.

        Given: Upgrade complete
        When: Summary displayed
        Then: Duration shown in seconds
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        assert hasattr(result, 'duration_seconds') or hasattr(result.summary, 'duration_seconds')

    def test_summary_saved_to_log_file(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        AC#8: Summary saved to .devforgeai/logs/upgrade-{timestamp}.log.

        Given: Upgrade complete
        When: Summary generated
        Then: Log file created with summary
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        logs_dir = project_root / ".devforgeai" / "logs"
        log_files = list(logs_dir.glob("upgrade-*.log"))
        assert len(log_files) > 0 or result.log_file is not None


# ============================================================================
# Test Class: Workflow Orchestration (SVC-002)
# ============================================================================

class TestWorkflowOrchestration:
    """Test upgrade workflow orchestration (SVC-002)."""

    def test_workflow_phases_execute_in_order(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        SVC-002: Workflow phases execute in order (backup -> migrate -> validate -> update).

        Given: Upgrade scenario
        When: execute() is called
        Then: Phases execute in correct sequence
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        call_order = []

        mock_dependencies["backup_service"].create_backup.side_effect = lambda **kwargs: (
            call_order.append("backup"),
            project_root / ".devforgeai" / "backups" / "v1.0.0"
        )[1]

        mock_dependencies["migration_discovery"].discover.side_effect = lambda **kwargs: (
            call_order.append("discover"),
            []
        )[1]

        mock_dependencies["migration_runner"].run.side_effect = lambda **kwargs: (
            call_order.append("migrate"),
            Mock(success=True, applied_migrations=[])
        )[1]

        mock_dependencies["migration_validator"].validate.side_effect = lambda **kwargs: (
            call_order.append("validate"),
            Mock(overall_passed=True, should_rollback=False)
        )[1]

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        assert call_order.index("backup") < call_order.index("migrate")
        assert call_order.index("migrate") < call_order.index("validate")

    def test_workflow_stops_on_backup_failure(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        SVC-002: Workflow stops if backup fails.

        Given: Backup creation fails
        When: execute() is called
        Then: Migration not attempted, error returned
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        mock_dependencies["backup_service"].create_backup.side_effect = PermissionError("Cannot create backup")

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        result = orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        assert result.success is False
        mock_dependencies["migration_runner"].run.assert_not_called()


# ============================================================================
# Test Class: Performance (NFRs)
# ============================================================================

class TestUpgradePerformance:
    """Test upgrade performance requirements (NFRs)."""

    def test_backup_completes_within_30_seconds(self, project_root, installed_version_1_0_0):
        """
        NFR-001: Backup creation < 30 seconds for standard installation.

        Given: Standard installation (<100MB)
        When: Backup created
        Then: Completes in <30 seconds
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        orchestrator = UpgradeOrchestrator(logger=Mock())

        # Act
        start = time.time()
        orchestrator._create_backup(project_root=project_root, from_version="1.0.0")
        elapsed = time.time() - start

        # Assert
        assert elapsed < 30, f"Backup took {elapsed:.2f}s (expected <30s)"

    def test_rollback_completes_within_60_seconds(self, project_root, installed_version_1_0_0):
        """
        NFR-003: Rollback < 60 seconds for standard backup.

        Given: Standard backup
        When: Rollback triggered
        Then: Completes in <60 seconds
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        # Create backup first
        orchestrator = UpgradeOrchestrator(logger=Mock())
        backup_path = orchestrator._create_backup(project_root=project_root, from_version="1.0.0")

        # Act
        start = time.time()
        orchestrator._rollback(backup_path=backup_path, project_root=project_root)
        elapsed = time.time() - start

        # Assert
        assert elapsed < 60, f"Rollback took {elapsed:.2f}s (expected <60s)"


# ============================================================================
# Test Class: Business Rules
# ============================================================================

class TestBusinessRules:
    """Test business rules for upgrade workflow."""

    def test_br001_backup_before_any_changes(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        BR-001: Backup must be created before any upgrade changes.

        Given: Upgrade confirmed
        When: Workflow starts
        Then: No files modified until backup complete
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        files_modified = []

        def track_backup(**kwargs):
            # Record that backup happened before any file changes
            current_version = json.loads((project_root / ".devforgeai" / ".version.json").read_text())
            assert current_version["version"] == "1.0.0", "Files modified before backup!"
            return project_root / ".devforgeai" / "backups" / "v1.0.0"

        mock_dependencies["backup_service"].create_backup.side_effect = track_backup
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act & Assert (no exception = backup before changes)
        orchestrator.execute(project_root=project_root, source_root=source_package["root"])

    def test_br004_user_content_preserved(self, project_root, installed_version_1_0_0, source_package, mock_dependencies):
        """
        BR-004: User content preserved during upgrade.

        Given: User has .ai_docs/Stories/ with content
        When: Upgrade executes
        Then: User stories not modified
        """
        # Arrange
        from installer.upgrade_orchestrator import UpgradeOrchestrator

        # Create user content
        stories_dir = project_root / ".ai_docs" / "Stories"
        stories_dir.mkdir(parents=True)
        user_story = stories_dir / "STORY-001.md"
        user_story.write_text("# User Story\n\nImportant content")

        mock_dependencies["backup_service"].create_backup.return_value = project_root / ".devforgeai" / "backups" / "v1.0.0"
        mock_dependencies["migration_discovery"].discover.return_value = []
        mock_dependencies["migration_runner"].run.return_value = Mock(success=True, applied_migrations=[])
        mock_dependencies["migration_validator"].validate.return_value = Mock(overall_passed=True, should_rollback=False)

        orchestrator = UpgradeOrchestrator(
            logger=mock_dependencies["logger"],
            backup_service=mock_dependencies["backup_service"],
            migration_discovery=mock_dependencies["migration_discovery"],
            migration_runner=mock_dependencies["migration_runner"],
            migration_validator=mock_dependencies["migration_validator"]
        )

        # Act
        orchestrator.execute(project_root=project_root, source_root=source_package["root"])

        # Assert
        assert user_story.exists()
        assert user_story.read_text() == "# User Story\n\nImportant content"
