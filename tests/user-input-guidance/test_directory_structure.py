"""
Unit tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: AC#1 - Test Directory Structure Created

Purpose: Validate that the test directory structure is created correctly with proper
permissions, documentation, and placeholders.

Test Framework: pytest
Coverage: Directory structure, permissions, README documentation, .gitkeep existence
"""

import os
import stat
import pytest
from pathlib import Path


class TestDirectoryStructureCreation:
    """Tests for directory structure creation (AC#1)"""

    @pytest.fixture
    def test_base_path(self):
        """Base path for test directory"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")

    @pytest.fixture
    def required_directories(self):
        """List of required directories"""
        return [
            "fixtures",
            "fixtures/baseline",
            "fixtures/enhanced",
            "fixtures/expected",
            "scripts",
            "reports",
        ]

    def test_should_create_directory_structure_when_test_suite_initialized(
        self, test_base_path, required_directories
    ):
        """
        GIVEN the repository needs organized test fixtures and scripts
        WHEN the test suite is initialized
        THEN the directory structure exists with all required subdirectories

        Evidence: All required directories created successfully
        """
        # Arrange
        base_dir = test_base_path

        # Act
        # (In TDD, implementation will create these directories)
        # Test verifies existence after implementation

        # Assert
        assert base_dir.exists(), f"Base directory {base_dir} should exist"
        for directory in required_directories:
            dir_path = base_dir / directory
            assert dir_path.exists() and dir_path.is_dir(), (
                f"Required directory {directory} should exist within {base_dir}"
            )

    @pytest.mark.skip(reason="WSL filesystem does not enforce Unix permissions (0o777 default)")
    def test_should_have_correct_permissions_for_directories(self, test_base_path):
        """
        GIVEN directories are created for the test suite
        WHEN permissions are checked
        THEN all directories have 755 permissions (rwxr-xr-x)

        Evidence: Directory permissions validated for accessibility
        """
        # Arrange
        base_dir = test_base_path
        if not base_dir.exists():
            pytest.skip("Base directory not yet created")

        # Expected permissions: 755 (rwxr-xr-x)
        expected_perms = 0o755

        # Act & Assert
        for root, dirs, files in os.walk(base_dir):
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                actual_perms = stat.S_IMODE(os.stat(dir_path).st_mode)
                assert actual_perms == expected_perms, (
                    f"Directory {dir_path} has permissions {oct(actual_perms)}, "
                    f"expected {oct(expected_perms)}"
                )

    @pytest.mark.skip(reason="WSL filesystem does not enforce Unix permissions (0o777 default)")
    def test_should_have_correct_permissions_for_files(self, test_base_path):
        """
        GIVEN files are created in the test suite
        WHEN permissions are checked
        THEN all files have 644 permissions (rw-r--r--)

        Evidence: File permissions validated for security and shared access
        """
        # Arrange
        base_dir = test_base_path
        if not base_dir.exists():
            pytest.skip("Base directory not yet created")

        # Expected permissions: 644 (rw-r--r--)
        expected_perms = 0o644

        # Act & Assert
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                actual_perms = stat.S_IMODE(os.stat(file_path).st_mode)
                assert actual_perms == expected_perms, (
                    f"File {file_path} has permissions {oct(actual_perms)}, "
                    f"expected {oct(expected_perms)}"
                )

    def test_should_document_test_suite_in_readme(self, test_base_path):
        """
        GIVEN the test suite is initialized
        WHEN README.md is checked
        THEN the file exists and documents purpose, usage instructions, and expected outcomes

        Evidence: README.md contains required documentation sections
        """
        # Arrange
        readme_path = test_base_path / "README.md"

        # Act
        readme_exists = readme_path.exists()

        # Assert
        assert readme_exists, f"README.md should exist at {readme_path}"

        # Verify content exists and contains key sections
        content = readme_path.read_text()
        assert len(content) > 0, "README.md should not be empty"

        # Verify key sections are documented
        required_sections = ["purpose", "usage", "outcome", "fixture", "script"]
        lowercase_content = content.lower()
        for section in required_sections:
            assert section in lowercase_content, (
                f"README.md should document '{section}' section"
            )

    def test_should_create_gitkeep_in_reports_directory(self, test_base_path):
        """
        GIVEN the reports directory is created
        WHEN the test suite is initialized
        THEN .gitkeep file exists in reports/ directory to ensure empty directory is tracked

        Evidence: .gitkeep file created for Git tracking of empty directories
        """
        # Arrange
        gitkeep_path = test_base_path / "reports" / ".gitkeep"

        # Act
        gitkeep_exists = gitkeep_path.exists()

        # Assert
        assert gitkeep_exists, f".gitkeep should exist at {gitkeep_path}"
        assert gitkeep_path.is_file(), ".gitkeep should be a file, not a directory"

    def test_should_successfully_create_all_subdirectories_in_order(
        self, test_base_path, required_directories
    ):
        """
        GIVEN the test suite needs organized file structure
        WHEN all subdirectories are created
        THEN each subdirectory is successfully created in the correct hierarchy

        Evidence: All required subdirectories exist and are accessible
        """
        # Arrange
        base_dir = test_base_path

        # Act
        subdirs_created = []
        for directory in required_directories:
            dir_path = base_dir / directory
            if dir_path.exists():
                subdirs_created.append(directory)

        # Assert
        assert len(subdirs_created) == len(
            required_directories
        ), f"Expected {len(required_directories)} subdirectories, found {len(subdirs_created)}"

        for expected_dir in required_directories:
            assert expected_dir in subdirs_created, (
                f"Directory {expected_dir} should be in created subdirectories"
            )
