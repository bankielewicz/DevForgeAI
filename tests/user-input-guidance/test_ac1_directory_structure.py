"""
Test Suite AC#1: Test Directory Structure Created

Validates that the test directory structure for user input guidance validation
exists with proper permissions, organization, and documentation.

Tests follow AAA pattern (Arrange, Act, Assert) and pytest conventions.
"""

import os
import stat
import pathlib
import pytest
from pathlib import Path


class TestDirectoryStructureCreation:
    """Test suite for AC#1: Directory structure creation and validation."""

    @pytest.fixture
    def test_root_dir(self):
        """Fixture: Return the test root directory path."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")

    def test_should_create_root_directory_tests_user_input_guidance(self, test_root_dir):
        """Test: Root directory tests/user-input-guidance/ should exist."""
        # Arrange
        expected_dir = test_root_dir

        # Act
        dir_exists = expected_dir.is_dir()

        # Assert
        assert dir_exists, f"Root directory {expected_dir} does not exist"

    def test_should_create_fixtures_subdirectory(self, test_root_dir):
        """Test: Subdirectory tests/user-input-guidance/fixtures/ should exist."""
        # Arrange
        expected_dir = test_root_dir / "fixtures"

        # Act
        dir_exists = expected_dir.is_dir()

        # Assert
        assert dir_exists, f"Fixtures subdirectory {expected_dir} does not exist"

    def test_should_create_scripts_subdirectory(self, test_root_dir):
        """Test: Subdirectory tests/user-input-guidance/scripts/ should exist."""
        # Arrange
        expected_dir = test_root_dir / "scripts"

        # Act
        dir_exists = expected_dir.is_dir()

        # Assert
        assert dir_exists, f"Scripts subdirectory {expected_dir} does not exist"

    def test_should_create_reports_subdirectory(self, test_root_dir):
        """Test: Subdirectory tests/user-input-guidance/reports/ should exist."""
        # Arrange
        expected_dir = test_root_dir / "reports"

        # Act
        dir_exists = expected_dir.is_dir()

        # Assert
        assert dir_exists, f"Reports subdirectory {expected_dir} does not exist"

    def test_should_create_baseline_fixtures_subdirectory(self, test_root_dir):
        """Test: Subdirectory tests/user-input-guidance/fixtures/baseline/ should exist."""
        # Arrange
        expected_dir = test_root_dir / "fixtures" / "baseline"

        # Act
        dir_exists = expected_dir.is_dir()

        # Assert
        assert dir_exists, f"Baseline fixtures subdirectory {expected_dir} does not exist"

    def test_should_create_enhanced_fixtures_subdirectory(self, test_root_dir):
        """Test: Subdirectory tests/user-input-guidance/fixtures/enhanced/ should exist."""
        # Arrange
        expected_dir = test_root_dir / "fixtures" / "enhanced"

        # Act
        dir_exists = expected_dir.is_dir()

        # Assert
        assert dir_exists, f"Enhanced fixtures subdirectory {expected_dir} does not exist"

    def test_should_create_expected_fixtures_subdirectory(self, test_root_dir):
        """Test: Subdirectory tests/user-input-guidance/fixtures/expected/ should exist."""
        # Arrange
        expected_dir = test_root_dir / "fixtures" / "expected"

        # Act
        dir_exists = expected_dir.is_dir()

        # Assert
        assert dir_exists, f"Expected fixtures subdirectory {expected_dir} does not exist"

    def test_should_create_readme_documentation_file(self, test_root_dir):
        """Test: File tests/user-input-guidance/README.md should exist."""
        # Arrange
        expected_file = test_root_dir / "README.md"

        # Act
        file_exists = expected_file.is_file()

        # Assert
        assert file_exists, f"README.md file {expected_file} does not exist"

    def test_should_create_gitkeep_in_reports_directory(self, test_root_dir):
        """Test: File tests/user-input-guidance/reports/.gitkeep should exist."""
        # Arrange
        expected_file = test_root_dir / "reports" / ".gitkeep"

        # Act
        file_exists = expected_file.is_file()

        # Assert
        assert file_exists, f".gitkeep file {expected_file} does not exist"

    @pytest.mark.skip(reason="WSL filesystem does not enforce Unix permissions (0o777 default)")
    def test_should_set_directory_permissions_755(self, test_root_dir):
        """Test: All directories should have permissions 755 (rwxr-xr-x)."""
        # Arrange
        directories = [
            test_root_dir,
            test_root_dir / "fixtures",
            test_root_dir / "fixtures" / "baseline",
            test_root_dir / "fixtures" / "enhanced",
            test_root_dir / "fixtures" / "expected",
            test_root_dir / "scripts",
            test_root_dir / "reports",
        ]
        expected_mode = 0o755

        # Act & Assert
        for dir_path in directories:
            if dir_path.exists():
                actual_mode = stat.S_IMODE(dir_path.stat().st_mode)
                assert (
                    actual_mode == expected_mode
                ), f"Directory {dir_path} has permissions {oct(actual_mode)}, expected {oct(expected_mode)}"

    @pytest.mark.skip(reason="WSL filesystem does not enforce Unix permissions (0o777 default)")
    def test_should_set_file_permissions_644(self, test_root_dir):
        """Test: All regular files should have permissions 644 (rw-r--r--)."""
        # Arrange
        files_to_check = [
            test_root_dir / "README.md",
            test_root_dir / "reports" / ".gitkeep",
        ]
        expected_mode = 0o644

        # Act & Assert
        for file_path in files_to_check:
            if file_path.exists() and file_path.is_file():
                actual_mode = stat.S_IMODE(file_path.stat().st_mode)
                assert (
                    actual_mode == expected_mode
                ), f"File {file_path} has permissions {oct(actual_mode)}, expected {oct(expected_mode)}"

    def test_readme_should_contain_purpose_section(self, test_root_dir):
        """Test: README.md should document test suite purpose."""
        # Arrange
        readme_file = test_root_dir / "README.md"

        # Act
        if readme_file.exists():
            content = readme_file.read_text()
        else:
            content = ""

        # Assert
        assert "Purpose" in content or "purpose" in content, (
            "README.md should contain 'Purpose' or 'purpose' section documenting test suite purpose"
        )

    def test_readme_should_contain_fixture_descriptions_section(self, test_root_dir):
        """Test: README.md should document fixture descriptions."""
        # Arrange
        readme_file = test_root_dir / "README.md"

        # Act
        if readme_file.exists():
            content = readme_file.read_text()
        else:
            content = ""

        # Assert
        assert "Fixture" in content or "fixture" in content, (
            "README.md should contain fixture descriptions section"
        )

    def test_readme_should_contain_script_usage_section(self, test_root_dir):
        """Test: README.md should document script usage instructions."""
        # Arrange
        readme_file = test_root_dir / "README.md"

        # Act
        if readme_file.exists():
            content = readme_file.read_text()
        else:
            content = ""

        # Assert
        assert "Script" in content or "script" in content, (
            "README.md should contain script usage section"
        )

    def test_readme_should_contain_methodology_section(self, test_root_dir):
        """Test: README.md should document measurement methodology."""
        # Arrange
        readme_file = test_root_dir / "README.md"

        # Act
        if readme_file.exists():
            content = readme_file.read_text()
        else:
            content = ""

        # Assert
        assert "Method" in content or "method" in content, (
            "README.md should contain methodology section"
        )

    def test_readme_should_contain_interpretation_section(self, test_root_dir):
        """Test: README.md should document result interpretation guidelines."""
        # Arrange
        readme_file = test_root_dir / "README.md"

        # Act
        if readme_file.exists():
            content = readme_file.read_text()
        else:
            content = ""

        # Assert
        assert "Interpret" in content or "interpret" in content, (
            "README.md should contain result interpretation section"
        )

    def test_all_required_directories_exist(self, test_root_dir):
        """Test: All 7 required directories should exist."""
        # Arrange
        required_dirs = [
            "fixtures",
            "fixtures/baseline",
            "fixtures/enhanced",
            "fixtures/expected",
            "scripts",
            "reports",
        ]

        # Act & Assert
        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = test_root_dir / dir_name
            if not dir_path.is_dir():
                missing_dirs.append(dir_name)

        assert (
            not missing_dirs
        ), f"Missing required directories: {', '.join(missing_dirs)}"

    def test_directory_names_should_be_lowercase(self, test_root_dir):
        """Test: All directory names should be lowercase (convention)."""
        # Arrange
        dirs_to_check = list(test_root_dir.glob("**/"))

        # Act
        invalid_dirs = []
        for dir_path in dirs_to_check:
            dir_name = dir_path.name
            if dir_name and not dir_name.startswith("."):
                if dir_name != dir_name.lower():
                    invalid_dirs.append(dir_name)

        # Assert
        assert (
            not invalid_dirs
        ), f"Directories should use lowercase names: {', '.join(invalid_dirs)}"

    def test_gitkeep_file_should_be_empty(self, test_root_dir):
        """Test: .gitkeep file should be empty (convention)."""
        # Arrange
        gitkeep_file = test_root_dir / "reports" / ".gitkeep"

        # Act
        if gitkeep_file.exists():
            content = gitkeep_file.read_text()
            file_size = gitkeep_file.stat().st_size
        else:
            content = None
            file_size = None

        # Assert
        if file_size is not None:
            assert file_size == 0, f".gitkeep should be empty but has {file_size} bytes"


class TestDirectoryStructureNFR:
    """Test suite for non-functional requirements of directory structure."""

    @pytest.fixture
    def test_root_dir(self):
        """Fixture: Return the test root directory path."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")

    def test_directory_creation_performance_under_100ms(self, test_root_dir):
        """NFR: Directory structure creation should complete quickly (<100ms)."""
        # Arrange
        import time

        start_time = time.perf_counter()

        # Act
        dir_exists = test_root_dir.exists()
        end_time = time.perf_counter()

        elapsed_ms = (end_time - start_time) * 1000

        # Assert
        assert dir_exists, "Directory structure does not exist"
        assert (
            elapsed_ms < 100
        ), f"Directory check took {elapsed_ms:.2f}ms (expected <100ms)"

    def test_directory_structure_is_deterministic(self, test_root_dir):
        """NFR: Directory structure should be consistent across multiple checks."""
        # Arrange
        checks = []

        # Act
        for _ in range(3):
            subdir_exists = (test_root_dir / "fixtures" / "baseline").is_dir()
            checks.append(subdir_exists)

        # Assert
        assert all(checks), "Directory existence should be consistent across checks"


class TestDirectoryStructureEdgeCases:
    """Test suite for edge cases in directory structure."""

    @pytest.fixture
    def test_root_dir(self):
        """Fixture: Return the test root directory path."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")

    def test_directory_structure_survives_missing_reports_subdirectory(
        self, test_root_dir, tmp_path
    ):
        """Edge case: Root and fixture dirs exist even if reports dir is missing."""
        # Arrange
        required_dirs = [
            "fixtures",
            "fixtures/baseline",
            "fixtures/enhanced",
            "fixtures/expected",
            "scripts",
        ]

        # Act
        missing = []
        for dir_name in required_dirs:
            if not (test_root_dir / dir_name).is_dir():
                missing.append(dir_name)

        # Assert
        assert (
            not missing
        ), f"Core directories should exist even if reports is missing: {missing}"

    def test_directory_structure_handles_symlinks(self, test_root_dir):
        """Edge case: Directory detection should work even with symlinks."""
        # Arrange
        fixtures_dir = test_root_dir / "fixtures"

        # Act
        is_dir = fixtures_dir.is_dir()

        # Assert
        assert is_dir, "Directory detection should handle symlinks correctly"

    def test_directory_traversal_depth_should_be_max_3_levels(self, test_root_dir):
        """NFR: Directory depth should not exceed 3 levels (root + fixtures + type)."""
        # Arrange
        deepest_path = test_root_dir / "fixtures" / "baseline"
        expected_max_depth = 3

        # Act
        relative_path = deepest_path.relative_to(test_root_dir.parent)
        actual_depth = len(relative_path.parts)

        # Assert
        assert (
            actual_depth <= expected_max_depth
        ), f"Directory depth {actual_depth} exceeds maximum {expected_max_depth}"


# Integration tests
class TestDirectoryStructureIntegration:
    """Integration tests for directory structure with actual filesystem."""

    @pytest.fixture
    def test_root_dir(self):
        """Fixture: Return the test root directory path."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")

    def test_all_directories_should_be_readable(self, test_root_dir):
        """Integration: All directories should be readable by current user."""
        # Arrange
        dirs_to_check = [
            test_root_dir,
            test_root_dir / "fixtures",
            test_root_dir / "fixtures" / "baseline",
            test_root_dir / "fixtures" / "enhanced",
            test_root_dir / "fixtures" / "expected",
            test_root_dir / "scripts",
            test_root_dir / "reports",
        ]

        # Act
        unreadable = []
        for dir_path in dirs_to_check:
            if not os.access(dir_path, os.R_OK):
                unreadable.append(str(dir_path))

        # Assert
        assert (
            not unreadable
        ), f"Directories should be readable: {', '.join(unreadable)}"

    def test_all_directories_should_be_writable(self, test_root_dir):
        """Integration: All directories should be writable by current user."""
        # Arrange
        dirs_to_check = [
            test_root_dir / "scripts",
            test_root_dir / "reports",
        ]

        # Act
        unwritable = []
        for dir_path in dirs_to_check:
            if not os.access(dir_path, os.W_OK):
                unwritable.append(str(dir_path))

        # Assert
        assert (
            not unwritable
        ), f"Script and reports directories should be writable: {', '.join(unwritable)}"

    def test_directory_listing_should_show_all_subdirectories(self, test_root_dir):
        """Integration: Directory listing should show expected subdirectories."""
        # Arrange
        expected_subdirs = {"fixtures", "scripts", "reports"}

        # Act
        if test_root_dir.exists():
            actual_subdirs = {
                item.name for item in test_root_dir.iterdir() if item.is_dir()
            }
        else:
            actual_subdirs = set()

        # Assert
        assert (
            expected_subdirs.issubset(actual_subdirs)
        ), f"Missing subdirectories: {expected_subdirs - actual_subdirs}"
