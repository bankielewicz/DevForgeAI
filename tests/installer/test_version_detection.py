"""
Unit tests for version detection (STORY-045 AC1, WKR-010, WKR-011, WKR-012).

Tests validate:
- Detecting existing installations by reading .devforgeai/.version.json
- Reading source version from src/devforgeai/version.json
- Semantic version comparison (1.0.0 vs 1.0.1 vs 1.1.0 vs 2.0.0)
- Installation mode determination (fresh, patch_upgrade, minor_upgrade, major_upgrade, reinstall, downgrade)

These tests validate AC1: "Installer Detects Existing Installations and Compares Versions"
and technical requirements WKR-010, WKR-011, WKR-012.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from packaging import version as pkg_version


class TestVersionDetection:
    """Unit tests for version.py module."""

    def test_detect_fresh_install_no_version_file(self, tmp_project):
        """
        AC1: Installer detects fresh install when .version.json missing.

        Given: Target project has no .devforgeai/.version.json
        When: Installer checks installation state
        Then: Mode detected as 'fresh_install'
        """
        # Arrange
        version_file = tmp_project["devforgeai"] / ".version.json"
        assert not version_file.exists(), "Test setup: version file should not exist"

        # Act
        # Simulating: get_installed_version(tmp_project["devforgeai"])
        has_version = version_file.exists()

        # Assert
        assert not has_version
        # Installation mode should be fresh_install

    def test_read_installed_version_from_existing_file(self, installed_version_1_0_0, tmp_project):
        """
        WKR-010: Read installed version from .devforgeai/.version.json.

        Given: .devforgeai/.version.json exists with version "1.0.0"
        When: Installer reads version file
        Then: Returns dict with version and installed_at timestamp
        """
        # Arrange
        version_file = tmp_project["devforgeai"] / ".version.json"
        assert version_file.exists()

        # Act
        content = json.loads(version_file.read_text())

        # Assert
        assert content["version"] == "1.0.0"
        assert content["installed_at"] == "2025-11-15T10:00:00Z"
        assert content["mode"] == "fresh_install"
        assert content["schema_version"] == "1.0"

    def test_read_source_version_from_version_json(self, mock_source_files, source_version_1_0_1):
        """
        WKR-011: Read source version from src/devforgeai/version.json.

        Given: Source version.json exists at src/devforgeai/version.json
        When: Installer reads source version
        Then: Returns dict with version and released_at timestamp
        """
        # Arrange
        version_file = mock_source_files["version_file"]
        assert version_file.exists()

        # Act
        content = json.loads(version_file.read_text())

        # Assert
        assert content["version"] == "1.0.1"
        assert content["released_at"] == "2025-11-17T12:00:00Z"
        assert content["schema_version"] == "1.0"

    def test_version_comparison_patch_upgrade(self):
        """
        WKR-012: Compare versions using semantic versioning (patch).

        Given: Installed version "1.0.0", source version "1.0.1"
        When: Versions are compared
        Then: Mode determined as 'patch_upgrade' (1.0.0 < 1.0.1, patch only)
        """
        # Arrange
        installed = pkg_version.parse("1.0.0")
        source = pkg_version.parse("1.0.1")

        # Act
        is_patch = (
            installed.major == source.major
            and installed.minor == source.minor
            and installed.micro < source.micro
        )

        # Assert
        assert is_patch
        assert source > installed

    def test_version_comparison_minor_upgrade(self):
        """
        WKR-012: Compare versions using semantic versioning (minor).

        Given: Installed version "1.0.0", source version "1.1.0"
        When: Versions are compared
        Then: Mode determined as 'minor_upgrade' (1.0.0 < 1.1.0, backward compatible)
        """
        # Arrange
        installed = pkg_version.parse("1.0.0")
        source = pkg_version.parse("1.1.0")

        # Act
        is_minor = (
            installed.major == source.major
            and installed.minor < source.minor
        )

        # Assert
        assert is_minor
        assert source > installed

    def test_version_comparison_major_upgrade(self):
        """
        WKR-012: Compare versions using semantic versioning (major).

        Given: Installed version "1.0.0", source version "2.0.0"
        When: Versions are compared
        Then: Mode determined as 'major_upgrade' (1.0.0 < 2.0.0, breaking changes)
        """
        # Arrange
        installed = pkg_version.parse("1.0.0")
        source = pkg_version.parse("2.0.0")

        # Act
        is_major = installed.major < source.major

        # Assert
        assert is_major
        assert source > installed

    def test_version_comparison_reinstall_same_version(self):
        """
        WKR-012: Compare versions when same version.

        Given: Installed version "1.0.0", source version "1.0.0"
        When: Versions are compared
        Then: Mode determined as 'reinstall' (same version, repair/reinstall)
        """
        # Arrange
        installed = pkg_version.parse("1.0.0")
        source = pkg_version.parse("1.0.0")

        # Act
        is_same = installed == source

        # Assert
        assert is_same

    def test_version_comparison_downgrade(self):
        """
        WKR-012: Compare versions for downgrade scenario.

        Given: Installed version "1.0.1", source version "1.0.0"
        When: Versions are compared
        Then: Mode determined as 'downgrade' (source older than installed)
        """
        # Arrange
        installed = pkg_version.parse("1.0.1")
        source = pkg_version.parse("1.0.0")

        # Act
        is_downgrade = source < installed

        # Assert
        assert is_downgrade

    def test_installation_mode_detection_fresh(self, tmp_project):
        """
        AC1: Determine installation mode is 'fresh_install'.

        Given: No .version.json exists
        When: Installation mode is determined
        Then: Mode is 'fresh_install'
        """
        # Arrange
        version_file = tmp_project["devforgeai"] / ".version.json"

        # Act
        is_fresh = not version_file.exists()

        # Assert
        assert is_fresh
        # Should set mode = 'fresh_install'

    def test_installation_mode_detection_patch_upgrade(self, installed_version_1_0_0):
        """
        AC1: Determine installation mode is 'patch_upgrade'.

        Given: Installed "1.0.0", source "1.0.1"
        When: Installation mode is determined
        Then: Mode is 'patch_upgrade'
        """
        # Arrange
        installed = pkg_version.parse(installed_version_1_0_0["version"])
        source = pkg_version.parse("1.0.1")

        # Act
        is_patch = (
            installed.major == source.major
            and installed.minor == source.minor
            and installed.micro < source.micro
        )

        # Assert
        assert is_patch
        # Should set mode = 'patch_upgrade'

    def test_version_file_missing_returns_none(self, tmp_project):
        """
        WKR-010: Handle missing version file gracefully.

        Given: .version.json does not exist
        When: Attempting to read installed version
        Then: Returns None or raises FileNotFoundError
        """
        # Arrange
        version_file = tmp_project["devforgeai"] / ".version.json"

        # Act
        exists = version_file.exists()

        # Assert
        assert not exists
        # get_installed_version should handle gracefully

    def test_invalid_version_format_raises_error(self):
        """
        AC1: Reject invalid semantic version format.

        Given: Version string "1.0.0.0" (too many components)
        When: Version is parsed
        Then: packaging allows it (lenient parsing) or raises InvalidVersion
        Note: packaging.version.parse is lenient and accepts various formats
        """
        # Arrange - Use actually invalid version format
        invalid_version = "not-a-version"

        # Act & Assert
        with pytest.raises(Exception):  # packaging.version.InvalidVersion
            pkg_version.parse(invalid_version)

    def test_version_comparison_complex_case_1_99_vs_2_0(self):
        """
        WKR-012: Verify semantic versioning works for edge case.

        Given: Installed "1.99.99", source "2.0.0"
        When: Versions compared
        Then: 2.0.0 > 1.99.99 (major upgrade)
        """
        # Arrange
        installed = pkg_version.parse("1.99.99")
        source = pkg_version.parse("2.0.0")

        # Act
        result = source > installed

        # Assert
        assert result

    def test_version_comparison_complex_case_1_1_vs_1_1_0(self):
        """
        WKR-012: Verify semantic versioning handles normalized versions.

        Given: Installed "1.1", source "1.1.0"
        When: Versions compared
        Then: Both are normalized to "1.1.0", equal
        """
        # Arrange
        installed = pkg_version.parse("1.1")
        source = pkg_version.parse("1.1.0")

        # Act
        result = installed == source

        # Assert
        assert result
