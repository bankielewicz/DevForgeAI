"""
Unit tests for MigrationDiscovery service (STORY-078).

Tests migration script discovery and ordering:
- Applicable migration identification (AC#3)
- Intermediate migration inclusion (AC#3)
- Version-based ordering (BR-002)
- Missing migration warnings (AC#3)

Test Framework: pytest 7.4+
Coverage Target: 95%+ for business logic
"""

import pytest
import logging
from pathlib import Path
from typing import List
from unittest.mock import MagicMock, patch

from installer.migration_discovery import MigrationDiscovery, StringVersionComparator
from installer.models import MigrationScript, MigrationError


class TestMigrationDiscovery:
    """Tests for SVC-008: Discover applicable migration scripts"""

    def test_should_discover_single_migration_for_patch_upgrade(self, tmp_path):
        """
        AC#3: Discover single migration for version change

        Arrange: migrations/v1.0.0-to-v1.0.1.py exists
        Act: Call discover(from_version="1.0.0", to_version="1.0.1")
        Assert: Returns [MigrationScript(v1.0.0-to-v1.0.1.py)]
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()
        migration_file = migrations_dir / "v1.0.0-to-v1.0.1.py"
        migration_file.write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.0.1")

        # Assert
        assert len(result) == 1
        assert result[0].from_version == "1.0.0"
        assert result[0].to_version == "1.0.1"

    def test_should_discover_direct_migration_for_minor_upgrade(self, tmp_path):
        """
        AC#3: Discover direct migration for minor version change

        Arrange: migrations/v1.0.0-to-v1.1.0.py exists
        Act: Call discover(from_version="1.0.0", to_version="1.1.0")
        Assert: Returns [MigrationScript(v1.0.0-to-v1.1.0.py)]
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()
        migration_file = migrations_dir / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.1.0")

        # Assert
        assert len(result) == 1
        assert result[0].from_version == "1.0.0"
        assert result[0].to_version == "1.1.0"

    def test_should_discover_direct_migration_for_major_upgrade(self, tmp_path):
        """
        AC#3: Discover direct migration for major version change

        Arrange: migrations/v1.0.0-to-v2.0.0.py exists
        Act: Call discover(from_version="1.0.0", to_version="2.0.0")
        Assert: Returns [MigrationScript(v1.0.0-to-v2.0.0.py)]
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()
        migration_file = migrations_dir / "v1.0.0-to-v2.0.0.py"
        migration_file.write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "2.0.0")

        # Assert
        assert len(result) == 1
        assert result[0].from_version == "1.0.0"
        assert result[0].to_version == "2.0.0"

    def test_should_return_empty_list_when_no_migrations_needed(self, tmp_path):
        """
        AC#3: Handle patch upgrade with no migrations

        Arrange: Upgrade 1.0.0 → 1.0.1 with no migration file
        Act: Call discover()
        Assert: Returns empty list (no migrations required)
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.0.1")

        # Assert
        assert result == []

    def test_should_follow_naming_convention_vX_Y_Z_to_vA_B_C(self, tmp_path):
        """
        AC#3: Migrations follow convention migrations/vX.Y.Z-to-vA.B.C.py

        Arrange: File migrations/v1.0.0-to-v1.1.0.py
        Act: Call discover()
        Assert: Correctly parses from_version and to_version from filename
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()
        migration_file = migrations_dir / "v1.0.0-to-v1.1.0.py"
        migration_file.write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.1.0")

        # Assert
        assert len(result) == 1
        assert result[0].from_version == "1.0.0"
        assert result[0].to_version == "1.1.0"

    def test_should_validate_migration_file_exists(self, tmp_path):
        """
        AC#3: Discovered migration file must exist

        Arrange: Missing migrations/v1.0.0-to-v1.1.0.py
        Act: Call discover()
        Assert: Does not return migration for non-existent file
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create MigrationScript with non-existent path will raise error
        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act - Try to discover with non-existent file
        result = discovery.discover("1.0.0", "1.1.0")

        # Assert
        assert result == []


class TestIntermediateMigrations:
    """Tests for SVC-008: Include intermediate migrations for version jumps"""

    def test_should_include_intermediate_migrations_for_minor_jump(self, tmp_path):
        """
        AC#3: Include intermediate migrations for version jumps

        Example: Upgrading 1.0.0 → 1.2.0 discovers:
        - migrations/v1.0.0-to-v1.1.0.py
        - migrations/v1.1.0-to-v1.2.0.py

        Arrange: Both migration files exist
        Act: Call discover(from_version="1.0.0", to_version="1.2.0")
        Assert: Returns [v1.0.0-to-v1.1.0.py, v1.1.0-to-v1.2.0.py]
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create intermediate migrations
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.2.0")

        # Assert
        assert len(result) == 2
        assert result[0].from_version == "1.0.0"
        assert result[0].to_version == "1.1.0"
        assert result[1].from_version == "1.1.0"
        assert result[1].to_version == "1.2.0"

    def test_should_include_three_intermediate_migrations_for_large_jump(self, tmp_path):
        """
        AC#3: Include all intermediate migrations for large version jump

        Arrange: Upgrade 1.0.0 → 1.3.0 with 3 migrations
        Act: Call discover(from_version="1.0.0", to_version="1.3.0")
        Assert: Returns all 3 migrations in sequence
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.2.0-to-v1.3.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.3.0")

        # Assert
        assert len(result) == 3
        assert result[0].to_version == "1.1.0"
        assert result[1].to_version == "1.2.0"
        assert result[2].to_version == "1.3.0"

    def test_should_handle_intermediate_migrations_across_minor_and_patch(self, tmp_path):
        """
        AC#3: Handle migrations across minor and patch versions

        Arrange: 1.0.0 → 1.1.0 → 1.1.1 → 1.2.0
        Act: Call discover(from_version="1.0.0", to_version="1.2.0")
        Assert: Returns all 3 migrations in correct order
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.0-to-v1.1.1.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.1-to-v1.2.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.2.0")

        # Assert
        assert len(result) == 3
        assert result[0].to_version == "1.1.0"
        assert result[1].to_version == "1.1.1"
        assert result[2].to_version == "1.2.0"

    def test_should_find_migration_chain_with_major_version_jump(self, tmp_path):
        """
        AC#3: Find intermediate migrations for major version jump

        Arrange: 1.0.0 → 1.5.0 → 2.0.0 (crossing major version)
        Act: Call discover(from_version="1.0.0", to_version="2.0.0")
        Assert: Returns migrations: 1.0 → 1.5, 1.5 → 2.0
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v1.5.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.5.0-to-v2.0.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "2.0.0")

        # Assert
        assert len(result) == 2
        assert result[0].from_version == "1.0.0"
        assert result[1].to_version == "2.0.0"

    def test_should_fail_if_migration_gap_exists(self, tmp_path, caplog):
        """
        AC#3: Missing migrations logged as warnings

        Arrange: Upgrade 1.0.0 → 1.3.0 but missing v1.1.0-to-v1.2.0.py
        Act: Call discover()
        Assert: Warning logged for missing migration, gaps identified
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create partial chain with gap
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        # v1.1.0-to-v1.2.0.py is MISSING
        (migrations_dir / "v1.2.0-to-v1.3.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        with caplog.at_level(logging.WARNING):
            result = discovery.discover("1.0.0", "1.3.0")

        # Assert
        # With gap, should return empty list (no valid path)
        assert result == []

    def test_should_log_warning_for_missing_intermediate_migration(self, tmp_path, caplog):
        """
        AC#3: Log warning when intermediate migration not found

        Arrange: Missing v1.1.0-to-v1.2.0.py in path
        Act: Call discover()
        Assert: Warning message includes missing version range
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        # v1.1.0-to-v1.2.0.py missing

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        with caplog.at_level(logging.WARNING):
            result = discovery.discover("1.0.0", "1.2.0")

        # Assert
        assert len(caplog.records) > 0  # Should have warning


class TestMigrationOrdering:
    """Tests for BR-002: Migrations execute in version order"""

    def test_should_order_migrations_by_from_version_ascending(self, tmp_path):
        """
        BR-002: Migrations execute in version order (oldest to newest)

        Arrange: 3 migration files in random filesystem order
        Act: Call discover()
        Assert: Returned in ascending order: v1.0→v1.1, v1.1→v1.2, v1.2→v1.3
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create in random order
        (migrations_dir / "v1.2.0-to-v1.3.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.3.0")

        # Assert - Must be in order
        assert len(result) == 3
        assert result[0].from_version == "1.0.0"
        assert result[1].from_version == "1.1.0"
        assert result[2].from_version == "1.2.0"

    def test_should_order_patch_versions_correctly(self, tmp_path):
        """
        BR-002: Patch versions ordered correctly (e.g., 1.0.1 before 1.0.2)

        Arrange: Migrations 1.0.0→1.0.1 and 1.0.1→1.0.2 (both from 1.0.0 start)
        Act: Call discover() with to_version=1.0.2
        Assert: Returns in order: 1.0.0→1.0.1, then 1.0.1→1.0.2
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v1.0.1.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.0.1-to-v1.0.2.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.0.2")

        # Assert
        assert len(result) == 2
        assert result[0].to_version == "1.0.1"
        assert result[1].to_version == "1.0.2"

    def test_should_order_minor_versions_correctly(self, tmp_path):
        """
        BR-002: Minor versions ordered correctly

        Arrange: Migrations 1.0→1.1, 1.1→1.2, 1.2→1.3
        Act: Call discover(from="1.0.0", to="1.3.0")
        Assert: Returned in sequence order
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.2.0-to-v1.3.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.3.0")

        # Assert
        assert len(result) == 3
        for i, migration in enumerate(result):
            assert migration.from_version == f"1.{i}.0"

    def test_should_order_major_versions_correctly(self, tmp_path):
        """
        BR-002: Major versions ordered correctly

        Arrange: Migrations 1.0→2.0, 2.0→3.0
        Act: Call discover(from="1.0.0", to="3.0.0")
        Assert: Returned in ascending order
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v2.0.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v2.0.0-to-v3.0.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "3.0.0")

        # Assert
        assert len(result) == 2
        assert result[0].from_version == "1.0.0"
        assert result[1].from_version == "2.0.0"

    def test_should_use_semver_comparison_for_ordering(self, tmp_path):
        """
        BR-002: Use semantic versioning for comparison

        Arrange: Migrations with versions 1.0.0, 1.0.1, 1.1.0, 2.0.0
        Act: Order migrations
        Assert: Correct semver ordering applied (not alphabetical)
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create in mixed order
        (migrations_dir / "v1.1.0-to-v2.0.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.0.0-to-v1.0.1.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.0.1-to-v1.1.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "2.0.0")

        # Assert - semver order, not alphabetical
        assert len(result) == 3
        assert result[0].to_version == "1.0.1"  # NOT "1.1.0" (alphabetical)
        assert result[1].to_version == "1.1.0"
        assert result[2].to_version == "2.0.0"

    def test_should_not_reorder_migrations_already_in_sequence(self, tmp_path):
        """
        BR-002: Already-ordered migrations remain in same order

        Arrange: Files listed in correct order by filesystem
        Act: Call discover()
        Assert: Order preserved (deterministic)
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act - Call multiple times
        result1 = discovery.discover("1.0.0", "1.2.0")
        result2 = discovery.discover("1.0.0", "1.2.0")

        # Assert - Deterministic
        assert result1[0].from_version == result2[0].from_version
        assert result1[1].from_version == result2[1].from_version


class TestMigrationEdgeCases:
    """Tests for edge cases and error scenarios"""

    def test_should_handle_empty_migrations_directory(self, tmp_path):
        """
        Edge case: No migrations exist for any version path

        Arrange: Upgrade 1.0.0 → 1.1.0 with empty migrations/
        Act: Call discover()
        Assert: Returns empty list gracefully
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.1.0")

        # Assert
        assert result == []

    def test_should_handle_migrations_directory_not_existing(self, tmp_path):
        """
        Edge case: migrations/ directory doesn't exist

        Arrange: Upgrade scenario with no migrations/ directory
        Act: Call discover()
        Assert: Raises MigrationError
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"  # Not created

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act & Assert
        with pytest.raises(MigrationError):
            discovery.discover("1.0.0", "1.1.0")

    def test_should_handle_malformed_migration_filenames(self, tmp_path):
        """
        Edge case: Files in migrations/ with incorrect naming

        Arrange: File named "migrate.py" (incorrect format)
        Act: Call discover()
        Assert: File skipped, not returned
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "migrate.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.1.0")

        # Assert - Should only get valid migration
        assert len(result) == 1
        assert result[0].from_version == "1.0.0"

    def test_should_ignore_non_python_files_in_migrations_dir(self, tmp_path):
        """
        Edge case: Non-Python files in migrations/ directory

        Arrange: migrations/ contains .txt, .md files
        Act: Call discover()
        Assert: Only .py files considered
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "README.md").write_text("# Migrations")
        (migrations_dir / "config.txt").write_text("config")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.1.0")

        # Assert
        assert len(result) == 1

    def test_should_ignore_hidden_files(self, tmp_path):
        """
        Edge case: Hidden files in migrations/ directory

        Arrange: migrations/ contains .hidden_migration.py
        Act: Call discover()
        Assert: Hidden files ignored
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / ".hidden_migration.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.1.0")

        # Assert - Only visible file
        assert len(result) == 1


# Fixtures for test support


@pytest.fixture
def migration_files(tmp_path):
    """Create test migration files"""
    migrations_dir = tmp_path / "migrations"
    migrations_dir.mkdir()

    # Create sample migration files
    migrations = [
        ("v1.0.0-to-v1.1.0.py", "1.0.0", "1.1.0"),
        ("v1.1.0-to-v1.2.0.py", "1.1.0", "1.2.0"),
        ("v1.2.0-to-v2.0.0.py", "1.2.0", "2.0.0"),
    ]

    for filename, from_ver, to_ver in migrations:
        script_content = f'''
def main():
    """Migration from {from_ver} to {to_ver}"""
    print("Running migration...")
    return {{"status": "success"}}

if __name__ == "__main__":
    main()
'''
        (migrations_dir / filename).write_text(script_content)

    return migrations_dir


@pytest.fixture
def version_comparator():
    """Version comparator service"""
    return StringVersionComparator()


@pytest.fixture
def discovery_scenario():
    """Typical migration discovery scenario"""
    return {
        "from_version": "1.0.0",
        "to_version": "1.2.0",
        "expected_migrations": [
            "v1.0.0-to-v1.1.0.py",
            "v1.1.0-to-v1.2.0.py",
        ]
    }


# ==================== NEW COVERAGE GAP TESTS (STORY-078 Phase 4.5) ====================
# Targets: 9% gap in migration_discovery.py (17 lines in validation/ordering)


class TestMigrationValidation:
    """Tests for migration validation edge cases"""

    def test_should_handle_invalid_version_format(self, tmp_path):
        """
        Test: Invalid version format rejected

        Arrange: Invalid version string "1.2"
        Act: Call discover()
        Assert: MigrationError raised
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act & Assert
        with pytest.raises(MigrationError) as exc_info:
            discovery.discover("1.2", "1.3.0")
        assert "version" in str(exc_info.value).lower()

    def test_should_handle_non_semver_versions(self, tmp_path):
        """
        Test: Non-semver versions rejected

        Arrange: Version with 4 parts "1.0.0.0"
        Act: Call discover()
        Assert: MigrationError raised
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act & Assert
        with pytest.raises(MigrationError):
            discovery.discover("1.0.0.0", "1.0.0.1")

    def test_should_detect_downgrade_attempt(self, tmp_path, caplog):
        """
        Test: Downgrade detected and rejected

        Arrange: from_version > to_version
        Act: Call discover()
        Assert: Returns empty list, warning logged
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        with caplog.at_level(logging.WARNING):
            result = discovery.discover("1.5.0", "1.0.0")

        # Assert
        assert result == []
        assert len(caplog.records) > 0

    def test_should_handle_same_version_upgrade(self, tmp_path):
        """
        Test: Upgrade to same version returns empty

        Arrange: from_version == to_version
        Act: Call discover()
        Assert: Returns empty list
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.0.0")

        # Assert
        assert result == []


class TestMigrationPathFinding:
    """Tests for BFS path finding edge cases"""

    def test_should_find_path_with_extra_migrations_in_directory(self, tmp_path):
        """
        Test: Find correct path when directory has unused migrations

        Arrange: Many migrations in directory, find shortest path
        Act: Call discover()
        Assert: Returns only applicable migrations
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create many migrations
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.2.0-to-v1.3.0.py").write_text("def main():\n    pass\n")

        # Create unrelated migrations
        (migrations_dir / "v2.0.0-to-v2.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v2.1.0-to-v2.2.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.2.0")

        # Assert
        assert len(result) == 2
        assert all(m.from_version.startswith("1") for m in result)

    def test_should_handle_disconnected_migration_paths(self, tmp_path, caplog):
        """
        Test: No path found between disconnected version chains

        Arrange: Two separate migration chains (1.x and 2.x), try to jump
        Act: Call discover()
        Assert: Returns empty list, warning logged
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Chain 1
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("def main():\n    pass\n")

        # Chain 2 (disconnected)
        (migrations_dir / "v2.0.0-to-v2.1.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        with caplog.at_level(logging.WARNING):
            result = discovery.discover("1.0.0", "2.1.0")

        # Assert
        assert result == []
        assert len(caplog.records) > 0

    def test_should_find_alternative_paths(self, tmp_path):
        """
        Test: BFS finds all alternative migration paths

        Arrange: Diamond pattern (1.0->1.1->1.3 OR 1.0->1.2->1.3)
        Act: Call discover()
        Assert: Returns one valid path
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Diamond path
        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.0.0-to-v1.2.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.1.0-to-v1.3.0.py").write_text("def main():\n    pass\n")
        (migrations_dir / "v1.2.0-to-v1.3.0.py").write_text("def main():\n    pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.3.0")

        # Assert
        assert len(result) == 2
        assert result[0].from_version == "1.0.0"
        assert result[1].to_version == "1.3.0"


class TestVersionComparison:
    """Tests for version comparison edge cases"""

    def test_should_compare_versions_with_equal_components(self):
        """
        Test: Equal version comparison

        Arrange: Same version
        Act: Call compare()
        Assert: Returns 0
        """
        # Arrange
        comparator = StringVersionComparator()

        # Act
        result = comparator.compare("1.0.0", "1.0.0")

        # Assert
        assert result == 0

    def test_should_compare_major_versions(self):
        """
        Test: Major version comparison

        Arrange: Different major versions
        Act: Call compare()
        Assert: Correct comparison result
        """
        # Arrange
        comparator = StringVersionComparator()

        # Act & Assert
        assert comparator.compare("1.0.0", "2.0.0") == -1
        assert comparator.compare("2.0.0", "1.0.0") == 1

    def test_should_compare_minor_versions(self):
        """
        Test: Minor version comparison

        Arrange: Different minor versions, same major
        Act: Call compare()
        Assert: Correct comparison result
        """
        # Arrange
        comparator = StringVersionComparator()

        # Act & Assert
        assert comparator.compare("1.1.0", "1.2.0") == -1
        assert comparator.compare("1.2.0", "1.1.0") == 1

    def test_should_compare_patch_versions(self):
        """
        Test: Patch version comparison

        Arrange: Different patch versions
        Act: Call compare()
        Assert: Correct comparison result
        """
        # Arrange
        comparator = StringVersionComparator()

        # Act & Assert
        assert comparator.compare("1.0.1", "1.0.2") == -1
        assert comparator.compare("1.0.2", "1.0.1") == 1


class TestMigrationDiscoveryCoverageGaps:
    """Tests to cover remaining uncovered lines in migration_discovery.py"""

    def test_default_migrations_directory_when_none(self, tmp_path, monkeypatch):
        """
        Test: Default migrations_dir uses ./migrations when None (covers line 94)

        Arrange: Change cwd to temp directory
        Act: Create MigrationDiscovery with migrations_dir=None
        Assert: migrations_dir defaults to cwd/migrations
        """
        # Arrange
        monkeypatch.chdir(tmp_path)

        # Act
        discovery = MigrationDiscovery(migrations_dir=None)

        # Assert
        expected = tmp_path / "migrations"
        assert discovery.migrations_dir == expected

    def test_discover_raises_error_when_path_is_not_directory(self, tmp_path):
        """
        Test: discover() raises MigrationError when path is file, not directory (covers line 116)

        Arrange: Pass a file path instead of directory
        Act: Call discover()
        Assert: MigrationError raised
        """
        # Arrange
        migrations_file = tmp_path / "migrations.txt"
        migrations_file.write_text("not a directory")

        discovery = MigrationDiscovery(migrations_dir=migrations_file)

        # Act & Assert
        with pytest.raises(MigrationError) as exc_info:
            discovery.discover("1.0.0", "1.1.0")
        assert "not a directory" in str(exc_info.value).lower()

    def test_discover_raises_error_when_directory_not_readable(self, tmp_path, monkeypatch):
        """
        Test: discover() raises MigrationError when directory not readable (covers line 118)

        Arrange: Mock os.access to return False
        Act: Call discover()
        Assert: MigrationError raised
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Mock os.access to simulate permission denied
        monkeypatch.setattr('os.access', lambda path, mode: False)

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act & Assert
        with pytest.raises(MigrationError) as exc_info:
            discovery.discover("1.0.0", "1.1.0")
        assert "not readable" in str(exc_info.value).lower()

    def test_scan_migration_files_returns_empty_when_directory_missing(self, tmp_path):
        """
        Test: _scan_migration_files returns empty when directory doesn't exist (covers line 221)

        Arrange: Non-existent migrations directory
        Act: Call _scan_migration_files
        Assert: Returns empty dict
        """
        # Arrange
        nonexistent_dir = tmp_path / "nonexistent"
        discovery = MigrationDiscovery(migrations_dir=tmp_path)

        # Act
        result = discovery._scan_migration_files(nonexistent_dir)

        # Assert
        assert result == {}

    def test_log_gaps_detects_version_gap_in_chain(self, tmp_path, caplog):
        """
        Test: _log_gaps detects missing migration in chain (covers line 342)

        Arrange: Migrations 1.0→1.1, 1.3→1.4 (missing 1.1→1.3)
        Act: Call _log_gaps
        Assert: Warning logged about gap
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create migrations with gap
        script1 = migrations_dir / "v1.0.0-to-v1.1.0.py"
        script1.write_text("# Migration")
        script2 = migrations_dir / "v1.3.0-to-v1.4.0.py"
        script2.write_text("# Migration")

        from installer.models import MigrationScript
        from installer.version_parser import Version
        migrations = [
            MigrationScript(path=str(script1), from_version="1.0.0", to_version="1.1.0"),
            MigrationScript(path=str(script2), from_version="1.3.0", to_version="1.4.0"),
        ]

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        with caplog.at_level("WARNING"):
            discovery._log_gaps(
                from_ver=Version(1, 0, 0),
                to_ver=Version(1, 4, 0),
                migrations=migrations
            )

        # Assert - Should log warning about gap from 1.1.0 to 1.3.0
        assert any("gap" in record.message.lower() for record in caplog.records)

    def test_log_gaps_detects_incomplete_migration_path(self, tmp_path, caplog):
        """
        Test: _log_gaps detects when migrations don't reach target (covers line 350)

        Arrange: Migrations end at 1.2.0 but target is 1.3.0
        Act: Call _log_gaps
        Assert: Warning logged about incomplete path
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create migration that stops before target
        script = migrations_dir / "v1.0.0-to-v1.2.0.py"
        script.write_text("# Migration")

        from installer.models import MigrationScript
        from installer.version_parser import Version
        migrations = [
            MigrationScript(path=str(script), from_version="1.0.0", to_version="1.2.0"),
        ]

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        with caplog.at_level("WARNING"):
            discovery._log_gaps(
                from_ver=Version(1, 0, 0),
                to_ver=Version(1, 3, 0),  # Target is 1.3.0, but migrations end at 1.2.0
                migrations=migrations
            )

        # Assert - Should log warning about incomplete path
        assert any("incomplete" in record.message.lower() for record in caplog.records)
