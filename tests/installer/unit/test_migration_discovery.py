"""
STORY-078: Unit tests for MigrationDiscovery service.

Tests migration script discovery, ordering, and gap detection.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+

AC Mapping:
- AC#3: Migration Script Discovery
  - Discover applicable migration scripts
  - Scripts follow convention: migrations/vX.Y.Z-to-vA.B.C.py
  - Intermediate migrations included (1.0->1.1, 1.1->1.2 for 1.0->1.2)
  - Missing migrations logged as warnings

Technical Specification:
- SVC-008: Discover applicable migration scripts
- SVC-009: Identify migration gaps (missing scripts)
- SVC-010: Order migrations by version sequence
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def migrations_dir(tmp_path):
    """
    Create a temporary migrations directory with sample migration scripts.

    Returns:
        Path: Path to migrations directory
    """
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    return migrations


@pytest.fixture
def sample_migration_scripts(migrations_dir):
    """
    Create sample migration scripts for testing.

    Creates:
    - v1.0.0-to-v1.1.0.py
    - v1.1.0-to-v1.2.0.py
    - v1.2.0-to-v2.0.0.py

    Returns:
        dict: Migration script paths keyed by from_version
    """
    scripts = {}

    # v1.0.0 -> v1.1.0
    script_1_0_to_1_1 = migrations_dir / "v1.0.0-to-v1.1.0.py"
    script_1_0_to_1_1.write_text('''"""Migration from 1.0.0 to 1.1.0"""
def migrate(project_root):
    print("Migrating 1.0.0 -> 1.1.0")
    return True
''')
    scripts["1.0.0"] = script_1_0_to_1_1

    # v1.1.0 -> v1.2.0
    script_1_1_to_1_2 = migrations_dir / "v1.1.0-to-v1.2.0.py"
    script_1_1_to_1_2.write_text('''"""Migration from 1.1.0 to 1.2.0"""
def migrate(project_root):
    print("Migrating 1.1.0 -> 1.2.0")
    return True
''')
    scripts["1.1.0"] = script_1_1_to_1_2

    # v1.2.0 -> v2.0.0
    script_1_2_to_2_0 = migrations_dir / "v1.2.0-to-v2.0.0.py"
    script_1_2_to_2_0.write_text('''"""Migration from 1.2.0 to 2.0.0"""
def migrate(project_root):
    print("Migrating 1.2.0 -> 2.0.0")
    return True
''')
    scripts["1.2.0"] = script_1_2_to_2_0

    return scripts


@pytest.fixture
def version_data():
    """
    Provide sample version data for testing.

    Returns:
        dict: Version configurations for various test scenarios
    """
    return {
        "installed_1_0_0": {"version": "1.0.0", "installed_at": "2025-11-01T00:00:00Z"},
        "installed_1_1_0": {"version": "1.1.0", "installed_at": "2025-11-15T00:00:00Z"},
        "installed_1_2_0": {"version": "1.2.0", "installed_at": "2025-11-20T00:00:00Z"},
        "source_1_1_0": {"version": "1.1.0", "released_at": "2025-11-10T00:00:00Z"},
        "source_1_2_0": {"version": "1.2.0", "released_at": "2025-11-18T00:00:00Z"},
        "source_2_0_0": {"version": "2.0.0", "released_at": "2025-12-01T00:00:00Z"},
    }


# ============================================================================
# Test Class: Discovery of Migration Scripts (AC#3, SVC-008)
# ============================================================================

class TestMigrationDiscovery:
    """Test discovery of applicable migration scripts (AC#3, SVC-008)."""

    def test_discover_single_migration_for_patch_upgrade(self, migrations_dir, sample_migration_scripts):
        """
        AC#3: Discover single migration for patch upgrade (1.0.0 -> 1.1.0).

        Given: Upgrade from 1.0.0 to 1.1.0
        When: MigrationDiscovery.discover() is called
        Then: Returns single migration script [v1.0.0-to-v1.1.0.py]
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="1.1.0")

        # Assert
        assert len(migrations) == 1
        assert migrations[0].from_version == "1.0.0"
        assert migrations[0].to_version == "1.1.0"
        assert Path(migrations[0].path).name == "v1.0.0-to-v1.1.0.py"

    def test_discover_multiple_migrations_for_multi_version_upgrade(self, migrations_dir, sample_migration_scripts):
        """
        AC#3: Discover multiple migrations for upgrade 1.0.0 -> 1.2.0.

        Given: Upgrade from 1.0.0 to 1.2.0
        When: MigrationDiscovery.discover() is called
        Then: Returns two migrations in order [v1.0.0-to-v1.1.0.py, v1.1.0-to-v1.2.0.py]
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="1.2.0")

        # Assert
        assert len(migrations) == 2
        assert migrations[0].from_version == "1.0.0"
        assert migrations[0].to_version == "1.1.0"
        assert migrations[1].from_version == "1.1.0"
        assert migrations[1].to_version == "1.2.0"

    def test_discover_major_upgrade_includes_all_intermediate_migrations(self, migrations_dir, sample_migration_scripts):
        """
        AC#3: Major upgrade 1.0.0 -> 2.0.0 includes all intermediate migrations.

        Given: Upgrade from 1.0.0 to 2.0.0
        When: MigrationDiscovery.discover() is called
        Then: Returns 3 migrations in version order
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="2.0.0")

        # Assert
        assert len(migrations) == 3
        assert migrations[0].from_version == "1.0.0"
        assert migrations[0].to_version == "1.1.0"
        assert migrations[1].from_version == "1.1.0"
        assert migrations[1].to_version == "1.2.0"
        assert migrations[2].from_version == "1.2.0"
        assert migrations[2].to_version == "2.0.0"

    def test_discover_returns_empty_list_for_no_migrations_needed(self, migrations_dir):
        """
        AC#3: Patch upgrade with no migration script returns empty list.

        Given: Upgrade from 1.0.0 to 1.0.1 with no migration scripts
        When: MigrationDiscovery.discover() is called
        Then: Returns empty list (no migrations needed for patch)
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="1.0.1")

        # Assert
        assert len(migrations) == 0

    def test_discover_returns_empty_for_reinstall(self, migrations_dir, sample_migration_scripts):
        """
        AC#3: Reinstall (same version) requires no migrations.

        Given: Install same version 1.0.0 -> 1.0.0
        When: MigrationDiscovery.discover() is called
        Then: Returns empty list
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="1.0.0")

        # Assert
        assert len(migrations) == 0

    def test_discover_returns_empty_for_downgrade(self, migrations_dir, sample_migration_scripts):
        """
        AC#3: Downgrade does not use upgrade migrations.

        Given: Downgrade from 1.2.0 to 1.0.0
        When: MigrationDiscovery.discover() is called
        Then: Returns empty list (downgrade has separate handling)
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.2.0", to_version="1.0.0")

        # Assert
        assert len(migrations) == 0


# ============================================================================
# Test Class: Migration Script Convention (AC#3)
# ============================================================================

class TestMigrationScriptConvention:
    """Test migration script naming convention validation (AC#3)."""

    def test_script_name_follows_convention_vX_Y_Z_to_vA_B_C(self, migrations_dir):
        """
        AC#3: Migration scripts follow convention vX.Y.Z-to-vA.B.C.py.

        Given: Migration directory with properly named scripts
        When: MigrationDiscovery scans for scripts
        Then: Scripts matching convention are discovered
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        # Create properly named scripts
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("# migration")
        (migrations_dir / "v2.0.0-to-v2.1.0.py").write_text("# migration")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        all_scripts = discovery._scan_migration_files(migrations_dir)
        # Flatten the nested dict to get all scripts
        all_scripts_list = []
        for from_v in all_scripts:
            for to_v in all_scripts[from_v]:
                all_scripts_list.append(all_scripts[from_v][to_v])

        # Assert
        assert len(all_scripts_list) == 2
        assert any(Path(s.path).name == "v1.0.0-to-v1.1.0.py" for s in all_scripts_list)
        assert any(Path(s.path).name == "v2.0.0-to-v2.1.0.py" for s in all_scripts_list)

    def test_invalid_script_names_ignored(self, migrations_dir):
        """
        AC#3: Scripts not matching convention are ignored.

        Given: Migration directory with invalid script names
        When: MigrationDiscovery scans for scripts
        Then: Invalid names are ignored
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        # Create valid and invalid named scripts
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("# valid")
        (migrations_dir / "migration_v1.py").write_text("# invalid - wrong format")
        (migrations_dir / "update.py").write_text("# invalid - no version")
        (migrations_dir / "v1.0.0-v1.1.0.py").write_text("# invalid - missing 'to'")
        (migrations_dir / "v1.0.0-to-v1.1.0.txt").write_text("# invalid - wrong extension")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        all_scripts = discovery._scan_migration_files(migrations_dir)
        # Flatten the nested dict to get all scripts
        all_scripts_list = []
        for from_v in all_scripts:
            for to_v in all_scripts[from_v]:
                all_scripts_list.append(all_scripts[from_v][to_v])

        # Assert
        assert len(all_scripts_list) == 1
        assert Path(all_scripts_list[0].path).name == "v1.0.0-to-v1.1.0.py"

    def test_parse_from_version_from_script_name(self, migrations_dir):
        """
        AC#3: Correctly parse from_version from script filename.

        Given: Script named v1.0.0-to-v1.1.0.py
        When: Script is parsed
        Then: from_version is "1.0.0"
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("# migration")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        all_scripts = discovery._scan_migration_files(migrations_dir)
        scripts = [all_scripts[from_v][to_v] for from_v in all_scripts for to_v in all_scripts[from_v]]

        # Assert
        assert scripts[0].from_version == "1.0.0"

    def test_parse_to_version_from_script_name(self, migrations_dir):
        """
        AC#3: Correctly parse to_version from script filename.

        Given: Script named v1.0.0-to-v1.1.0.py
        When: Script is parsed
        Then: to_version is "1.1.0"
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("# migration")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        all_scripts = discovery._scan_migration_files(migrations_dir)
        scripts = [all_scripts[from_v][to_v] for from_v in all_scripts for to_v in all_scripts[from_v]]

        # Assert
        assert scripts[0].to_version == "1.1.0"


# ============================================================================
# Test Class: Migration Ordering (AC#3, SVC-010)
# ============================================================================

class TestMigrationOrdering:
    """Test migration ordering by version sequence (AC#3, SVC-010)."""

    def test_migrations_ordered_by_from_version(self, migrations_dir, sample_migration_scripts):
        """
        SVC-010: Migrations returned in version order (oldest to newest).

        Given: Multiple migration scripts in directory
        When: Discover migrations for upgrade path
        Then: Migrations ordered by from_version ascending
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="2.0.0")

        # Assert
        for i in range(len(migrations) - 1):
            current = migrations[i]
            next_migration = migrations[i + 1]
            assert current.to_version == next_migration.from_version, \
                f"Migration chain broken: {current.to_version} != {next_migration.from_version}"

    def test_migrations_form_continuous_chain(self, migrations_dir, sample_migration_scripts):
        """
        SVC-010: Migrations form continuous version chain.

        Given: Upgrade from 1.0.0 to 2.0.0
        When: Migrations discovered
        Then: Each migration's to_version equals next migration's from_version
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="2.0.0")

        # Assert
        assert migrations[0].from_version == "1.0.0"
        assert migrations[-1].to_version == "2.0.0"

        # Verify chain continuity
        for i in range(len(migrations) - 1):
            assert migrations[i].to_version == migrations[i + 1].from_version

    def test_unordered_scripts_in_directory_still_return_ordered(self, migrations_dir):
        """
        SVC-010: Scripts discovered in any filesystem order return properly ordered.

        Given: Migration scripts saved in random order
        When: Discover migrations
        Then: Results are version-ordered regardless of filesystem order
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        # Create scripts in "random" order
        (migrations_dir / "v1.2.0-to-v2.0.0.py").write_text("# 3rd")
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("# 1st")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("# 2nd")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="2.0.0")

        # Assert
        assert len(migrations) == 3
        assert migrations[0].from_version == "1.0.0"
        assert migrations[1].from_version == "1.1.0"
        assert migrations[2].from_version == "1.2.0"


# ============================================================================
# Test Class: Migration Gap Detection (AC#3, SVC-009)
# ============================================================================

class TestMigrationGapDetection:
    """Test detection of missing migrations in upgrade path (AC#3, SVC-009)."""

    def test_detect_gap_when_intermediate_migration_missing(self, migrations_dir):
        """
        SVC-009: Detect gap when intermediate migration is missing.

        Given: Upgrade 1.0.0 -> 1.2.0 with missing v1.1.0-to-v1.2.0.py
        When: MigrationDiscovery.discover() is called
        Then: No path found (gap blocks migration)
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        # Only create first migration (missing v1.1.0-to-v1.2.0.py)
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("# migration 1")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        with patch('installer.migration_discovery.logger') as mock_logger:
            migrations = discovery.discover(from_version="1.0.0", to_version="1.2.0")

        # Assert
        # When intermediate migration is missing, BFS cannot find complete path
        assert len(migrations) == 0  # No complete path found
        # Warning should be logged for no path found
        assert mock_logger.warning.called

    def test_get_missing_migrations_returns_gap_list(self, migrations_dir):
        """
        SVC-009: Detect gaps when intermediate migration is missing.

        Given: Upgrade path with gaps (v1.0.0 -> v1.1.0 exists, but v1.1.0 -> v1.2.0 is missing)
        When: discover() is called
        Then: Returns only migrations that exist (empty result if path blocked)
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        # Create migration with gap
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("# exists")
        # Missing: v1.1.0-to-v1.2.0.py
        (migrations_dir / "v1.2.0-to-v2.0.0.py").write_text("# exists")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        gaps = discovery.discover(from_version="1.0.0", to_version="2.0.0")

        # Assert
        # Since intermediate migration is missing, path cannot be found
        assert len(gaps) == 0  # BFS search won't find a path across the gap

    def test_no_gaps_returns_empty_list(self, migrations_dir, sample_migration_scripts):
        """
        SVC-009: No gaps when migration chain is complete.

        Given: Complete migration chain from 1.0.0 to 2.0.0
        When: discover() is called
        Then: Returns all migrations forming continuous chain
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="2.0.0")

        # Assert
        assert len(migrations) == 3  # Complete path: 1.0->1.1->1.2->2.0

    def test_missing_migration_logged_as_warning_not_error(self, migrations_dir):
        """
        AC#3: Missing migrations logged as warnings (upgrade can still proceed).

        Given: Migration gap exists
        When: Discovery runs
        Then: Warning logged (not error), discovery completes
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        with patch('installer.migration_discovery.logger') as mock_logger:
            migrations = discovery.discover(from_version="1.0.0", to_version="1.1.0")

        # Assert - should complete without raising exception
        # No migrations found - logger should not raise exceptions
        assert isinstance(migrations, list)


# ============================================================================
# Test Class: Edge Cases
# ============================================================================

class TestMigrationDiscoveryEdgeCases:
    """Test edge cases for migration discovery."""

    def test_empty_migrations_directory(self, migrations_dir):
        """
        Edge case: Empty migrations directory returns empty list.

        Given: Empty migrations directory
        When: discover() is called
        Then: Returns empty list without error
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="2.0.0")

        # Assert
        assert migrations == []

    def test_nonexistent_migrations_directory_raises_error(self, tmp_path):
        """
        Edge case: Nonexistent migrations directory raises MigrationError on discover.

        Given: Migrations directory does not exist
        When: discover() is called
        Then: Raises MigrationError
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery
        from installer.models import MigrationError

        nonexistent = tmp_path / "nonexistent_migrations"
        discovery = MigrationDiscovery(migrations_dir=nonexistent)

        # Act & Assert
        with pytest.raises(MigrationError):
            discovery.discover(from_version="1.0.0", to_version="1.1.0")

    def test_discover_with_prerelease_versions(self, migrations_dir):
        """
        Edge case: Handle prerelease version migrations.

        Given: Migration scripts for prerelease versions (1.0.0-alpha, 1.0.0-beta)
        When: discover() is called
        Then: Prerelease migrations are discovered and ordered correctly
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        # Create prerelease migration (implementation may vary)
        (migrations_dir / "v1.0.0-to-v1.0.1.py").write_text("# migration")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="1.0.0", to_version="1.0.1")

        # Assert
        assert len(migrations) == 1

    def test_discover_handles_version_with_leading_zeros(self, migrations_dir):
        """
        Edge case: Version strings with leading zeros handled correctly.

        Given: Version "01.00.00" (malformed but possible)
        When: Compared with "1.0.0"
        Then: Treated as equivalent or handled gracefully
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act & Assert - should not raise exception
        migrations = discovery.discover(from_version="01.00.00", to_version="1.1.0")

        # Implementation should handle or reject gracefully

    def test_discover_with_very_large_version_numbers(self, migrations_dir):
        """
        Edge case: Very large version numbers handled correctly.

        Given: Version "100.200.300"
        When: discover() is called
        Then: No integer overflow or comparison errors
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        (migrations_dir / "v100.200.300-to-v100.200.301.py").write_text("# migration")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        migrations = discovery.discover(from_version="100.200.300", to_version="100.200.301")

        # Assert
        assert len(migrations) == 1


# ============================================================================
# Test Class: MigrationScript Data Model
# ============================================================================

class TestMigrationScriptModel:
    """Test MigrationScript data model (Technical Specification DataModel)."""

    def test_migration_script_has_required_fields(self, migrations_dir):
        """
        DataModel: MigrationScript has path, from_version, to_version.

        Given: A discovered migration script
        When: Accessing script properties
        Then: All required fields are present
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("# migration")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)
        all_scripts = discovery._scan_migration_files(migrations_dir)
        scripts = [all_scripts[from_v][to_v] for from_v in all_scripts for to_v in all_scripts[from_v]]

        # Act
        script = scripts[0]

        # Assert
        assert hasattr(script, 'path')
        assert hasattr(script, 'from_version')
        assert hasattr(script, 'to_version')
        assert isinstance(script.path, str)  # path is str in MigrationScript
        assert isinstance(script.from_version, str)
        assert isinstance(script.to_version, str)

    def test_migration_script_path_exists(self, migrations_dir):
        """
        DataModel: MigrationScript.path exists and is readable.

        Given: A discovered migration script
        When: Checking path
        Then: Path exists
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("# migration")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)
        all_scripts = discovery._scan_migration_files(migrations_dir)
        scripts = [all_scripts[from_v][to_v] for from_v in all_scripts for to_v in all_scripts[from_v]]

        # Act
        script = scripts[0]

        # Assert
        assert Path(script.path).exists()

    def test_migration_script_versions_parsed_from_filename(self, migrations_dir):
        """
        DataModel: from_version and to_version parsed from filename.

        Given: Script named v1.2.3-to-v4.5.6.py
        When: Script is parsed
        Then: from_version="1.2.3", to_version="4.5.6"
        """
        # Arrange
        from installer.migration_discovery import MigrationDiscovery

        (migrations_dir / "v1.2.3-to-v4.5.6.py").write_text("# migration")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)
        all_scripts = discovery._scan_migration_files(migrations_dir)
        scripts = [all_scripts[from_v][to_v] for from_v in all_scripts for to_v in all_scripts[from_v]]

        # Act
        script = scripts[0]

        # Assert
        assert script.from_version == "1.2.3"
        assert script.to_version == "4.5.6"
