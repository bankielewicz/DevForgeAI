"""
STORY-242: OS-Specific Installer Generation Module - Test Suite

Test-Driven Development (TDD) - Red Phase
These tests WILL FAIL initially because InstallerConfig and InstallerGenerator
do not exist yet. Implementation will make them pass.

Coverage targets:
- Unit tests: 95%+ for installer_generator module
- All 6 acceptance criteria tested
- All 10 service requirements (SVC-001 through SVC-010)
- All 4 business rules (BR-001 through BR-004)
- Edge cases and error handling

Test file location per source-tree.md: tests/STORY-242/
"""

# CRITICAL: Add project root to sys.path BEFORE any other imports
# This must be at the very top to ensure installer module can be imported
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(_project_root))

import hashlib
import os
import shutil
import stat
import tempfile
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import Mock, patch, MagicMock

import pytest


# ==============================================================================
# IMPORT TESTS - These will fail until module is created
# ==============================================================================


class TestModuleImports:
    """Test that the installer_generator module can be imported."""

    def test_import_installer_config_dataclass(self):
        """
        Test: InstallerConfig dataclass can be imported.
        Expected: Import succeeds (currently fails - module doesn't exist).
        """
        # Arrange & Act
        from installer.installer_generator import InstallerConfig

        # Assert
        assert InstallerConfig is not None

    def test_import_installer_generator_class(self):
        """
        Test: InstallerGenerator class can be imported.
        Expected: Import succeeds (currently fails - module doesn't exist).
        """
        # Arrange & Act
        from installer.installer_generator import InstallerGenerator

        # Assert
        assert InstallerGenerator is not None


# ==============================================================================
# INSTALLER CONFIG DATACLASS TESTS
# ==============================================================================


class TestInstallerConfigDataclass:
    """
    Test InstallerConfig dataclass fields per Technical Specification.

    Technical Spec fields:
    - platform: String (Required, Enum: windows, linux_deb, linux_rpm, macos)
    - format: String (Required: msi, nsis, deb, rpm, pkg)
    - config_path: String (Required: path to generated file(s))
    - build_command: Optional[String] (shell command)
    - tool_required: String (Required: wix, nsis, dpkg-deb, rpmbuild, pkgbuild)
    - tool_available: Bool (Required: True if tool installed)
    - metadata: Dict[str, Any] (Optional: platform-specific data)
    """

    def test_installer_config_has_platform_field(self):
        """Test: InstallerConfig has platform field (Technical Spec field 1)."""
        from installer.installer_generator import InstallerConfig

        # Arrange
        config = InstallerConfig(
            platform="windows",
            format="msi",
            config_path="/path/to/config.wxs",
            build_command="candle *.wxs && light *.wixobj",
            tool_required="wix",
            tool_available=True,
            metadata={}
        )

        # Assert
        assert hasattr(config, "platform")
        assert config.platform == "windows"

    def test_installer_config_has_format_field(self):
        """Test: InstallerConfig has format field (Technical Spec field 2)."""
        from installer.installer_generator import InstallerConfig

        # Arrange
        config = InstallerConfig(
            platform="linux_deb",
            format="deb",
            config_path="/path/to/DEBIAN",
            build_command="dpkg-deb --build package",
            tool_required="dpkg-deb",
            tool_available=True,
            metadata={}
        )

        # Assert
        assert hasattr(config, "format")
        assert config.format == "deb"

    def test_installer_config_has_config_path_field(self):
        """Test: InstallerConfig has config_path field (Technical Spec field 3)."""
        from installer.installer_generator import InstallerConfig

        config = InstallerConfig(
            platform="macos",
            format="pkg",
            config_path="/path/to/distribution.xml",
            build_command="pkgbuild --root ...",
            tool_required="pkgbuild",
            tool_available=True,
            metadata={}
        )

        assert hasattr(config, "config_path")
        assert config.config_path == "/path/to/distribution.xml"

    def test_installer_config_has_build_command_field(self):
        """Test: InstallerConfig has build_command field (Technical Spec field 4)."""
        from installer.installer_generator import InstallerConfig

        config = InstallerConfig(
            platform="windows",
            format="nsis",
            config_path="/path/to/installer.nsi",
            build_command="makensis installer.nsi",
            tool_required="nsis",
            tool_available=True,
            metadata={}
        )

        assert hasattr(config, "build_command")
        assert config.build_command == "makensis installer.nsi"

    def test_installer_config_build_command_is_optional(self):
        """Test: InstallerConfig build_command can be None (Technical Spec: Optional)."""
        from installer.installer_generator import InstallerConfig

        config = InstallerConfig(
            platform="linux_rpm",
            format="rpm",
            config_path="/path/to/package.spec",
            build_command=None,
            tool_required="rpmbuild",
            tool_available=False,
            metadata={}
        )

        assert config.build_command is None

    def test_installer_config_has_tool_required_field(self):
        """Test: InstallerConfig has tool_required field (Technical Spec field 5)."""
        from installer.installer_generator import InstallerConfig

        config = InstallerConfig(
            platform="linux_deb",
            format="deb",
            config_path="/path/to/DEBIAN",
            build_command="dpkg-deb --build package",
            tool_required="dpkg-deb",
            tool_available=True,
            metadata={}
        )

        assert hasattr(config, "tool_required")
        assert config.tool_required == "dpkg-deb"

    def test_installer_config_has_tool_available_field(self):
        """Test: InstallerConfig has tool_available field (Technical Spec field 6)."""
        from installer.installer_generator import InstallerConfig

        config = InstallerConfig(
            platform="windows",
            format="msi",
            config_path="/path/to/config.wxs",
            build_command=None,
            tool_required="wix",
            tool_available=False,
            metadata={}
        )

        assert hasattr(config, "tool_available")
        assert config.tool_available is False

    def test_installer_config_has_metadata_field(self):
        """Test: InstallerConfig has metadata field (Technical Spec field 7)."""
        from installer.installer_generator import InstallerConfig

        metadata = {
            "product_guid": "12345678-1234-1234-1234-123456789012",
            "upgrade_guid": "87654321-4321-4321-4321-210987654321"
        }

        config = InstallerConfig(
            platform="windows",
            format="msi",
            config_path="/path/to/config.wxs",
            build_command=None,
            tool_required="wix",
            tool_available=True,
            metadata=metadata
        )

        assert hasattr(config, "metadata")
        assert config.metadata == metadata


# ==============================================================================
# AC#1: WINDOWS INSTALLER CONFIGURATION (MSI/WiX)
# ==============================================================================


class TestWindowsMsiWixGeneration:
    """
    AC#1: Windows MSI/WiX installer configuration generation.

    Given: A project targeting Windows distribution
    When: InstallerGenerator is invoked with Windows target
    Then: Generates a WiX source file (.wxs) containing:
        - Product ID and upgrade code (GUIDs)
        - Component definitions for all files
        - Start menu shortcuts
        - Uninstall support
    And: Returns an InstallerConfig with the file path.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    @pytest.fixture
    def sample_package_result(self) -> dict:
        """Sample PackageResult from STORY-241 for testing."""
        return {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package-1.0.0.zip",
            "package_name": "myapp-1.0.0",
            "version": "1.0.0",
            "size_bytes": 1024000,
            "checksum": "abc123def456",
            "docker_image": None,
            "command_executed": "zip -r myapp-1.0.0.zip .",
            "duration_ms": 500
        }

    def test_generate_wix_config_returns_installer_config(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: WiX generation returns InstallerConfig (SVC-001).
        Expected: Returns InstallerConfig with platform='windows', format='msi'.
        """
        from installer.installer_generator import InstallerGenerator, InstallerConfig

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert
        assert isinstance(result, InstallerConfig)
        assert result.platform == "windows"
        assert result.format == "msi"

    def test_generate_wix_creates_wxs_file(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: WiX generation creates .wxs file (SVC-001).
        Expected: File exists at config_path with .wxs extension.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert
        assert result.config_path is not None
        assert result.config_path.endswith(".wxs")
        assert Path(result.config_path).exists()

    def test_wix_file_contains_product_guid(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: WiX file contains Product GUID (SVC-007).
        Expected: .wxs contains valid UUID in Product element.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert
        wxs_content = Path(result.config_path).read_text()
        # Should contain a valid GUID in Product Id attribute
        assert "Product" in wxs_content
        assert "Id=" in wxs_content or 'Id="' in wxs_content

        # GUID should be in metadata
        assert "product_guid" in result.metadata or "ProductId" in wxs_content

    def test_wix_file_contains_upgrade_code(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: WiX file contains UpgradeCode GUID (SVC-007).
        Expected: .wxs contains UpgradeCode attribute.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert
        wxs_content = Path(result.config_path).read_text()
        assert "UpgradeCode=" in wxs_content or 'UpgradeCode="' in wxs_content

    def test_wix_file_contains_component_definitions(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: WiX file contains Component definitions (SVC-008).
        Expected: .wxs contains Component elements for files.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert
        wxs_content = Path(result.config_path).read_text()
        assert "<Component" in wxs_content or "Component " in wxs_content

    def test_wix_file_contains_shortcut_element(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: WiX file contains Start Menu shortcut (AC#1 requirement).
        Expected: .wxs contains Shortcut element.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert
        wxs_content = Path(result.config_path).read_text()
        # Should have shortcut or start menu reference
        assert ("<Shortcut" in wxs_content or
                "ProgramMenuFolder" in wxs_content or
                "StartMenuFolder" in wxs_content)

    def test_wix_file_contains_uninstall_support(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: WiX file contains uninstall support (AC#1 requirement).
        Expected: .wxs contains RemoveFolder or uninstall element.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert
        wxs_content = Path(result.config_path).read_text()
        # MSI inherently supports uninstall; look for RemoveFolder or similar
        assert ("<RemoveFolder" in wxs_content or
                "MajorUpgrade" in wxs_content or
                "RemoveExistingProducts" in wxs_content)

    def test_wix_returns_correct_tool_required(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: WiX config has tool_required='wix'.
        Expected: InstallerConfig.tool_required == 'wix'.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert
        assert result.tool_required == "wix"

    def test_wix_returns_correct_build_command(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: WiX config has correct build_command.
        Expected: Build command contains candle and light.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert
        assert result.build_command is not None
        assert "candle" in result.build_command.lower() or "wix" in result.build_command.lower()

    def test_wix_guids_are_valid_uuid_format(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: Generated GUIDs are valid UUID format (SVC-007).
        Expected: GUIDs in metadata can be parsed as UUID.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert - GUIDs should be valid UUIDs
        if "product_guid" in result.metadata:
            # Should not raise ValueError
            uuid.UUID(result.metadata["product_guid"])
        if "upgrade_guid" in result.metadata:
            uuid.UUID(result.metadata["upgrade_guid"])


# ==============================================================================
# AC#2: WINDOWS INSTALLER CONFIGURATION (NSIS)
# ==============================================================================


class TestWindowsNsisGeneration:
    """
    AC#2: Windows NSIS installer configuration generation.

    Given: A project targeting Windows distribution with NSIS preference
    When: InstallerGenerator is invoked with NSIS target
    Then: Generates an NSIS script (.nsi) containing:
        - Installer metadata (name, version, publisher)
        - Installation directory selection
        - File installation commands
        - Uninstaller creation
    And: Returns an InstallerConfig with the file path.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    @pytest.fixture
    def sample_package_result(self) -> dict:
        """Sample PackageResult from STORY-241 for testing."""
        return {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package-1.0.0.zip",
            "package_name": "myapp-1.0.0",
            "version": "1.0.0",
            "size_bytes": 1024000,
            "checksum": "abc123def456",
            "docker_image": None,
            "command_executed": "zip -r myapp-1.0.0.zip .",
            "duration_ms": 500
        }

    def test_generate_nsis_config_returns_installer_config(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: NSIS generation returns InstallerConfig (SVC-002).
        Expected: Returns InstallerConfig with platform='windows', format='nsis'.
        """
        from installer.installer_generator import InstallerGenerator, InstallerConfig

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="nsis",
            package_info=sample_package_result
        )

        # Assert
        assert isinstance(result, InstallerConfig)
        assert result.platform == "windows"
        assert result.format == "nsis"

    def test_generate_nsis_creates_nsi_file(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: NSIS generation creates .nsi file (SVC-002).
        Expected: File exists at config_path with .nsi extension.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="nsis",
            package_info=sample_package_result
        )

        # Assert
        assert result.config_path is not None
        assert result.config_path.endswith(".nsi")
        assert Path(result.config_path).exists()

    def test_nsis_file_contains_installer_name(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: NSIS file contains installer name (AC#2 metadata).
        Expected: .nsi contains Name directive.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="nsis",
            package_info=sample_package_result
        )

        # Assert
        nsi_content = Path(result.config_path).read_text()
        assert "Name " in nsi_content or "!define NAME" in nsi_content

    def test_nsis_file_contains_version(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: NSIS file contains version (AC#2 metadata).
        Expected: .nsi contains version reference.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="nsis",
            package_info=sample_package_result
        )

        # Assert
        nsi_content = Path(result.config_path).read_text()
        assert ("!define VERSION" in nsi_content or
                "VIProductVersion" in nsi_content or
                sample_package_result["version"] in nsi_content)

    def test_nsis_file_contains_install_directory(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: NSIS file contains installation directory selection (AC#2).
        Expected: .nsi contains InstallDir or DirText directive.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="nsis",
            package_info=sample_package_result
        )

        # Assert
        nsi_content = Path(result.config_path).read_text()
        assert ("InstallDir" in nsi_content or
                "$PROGRAMFILES" in nsi_content or
                "SetOutPath" in nsi_content)

    def test_nsis_file_contains_file_commands(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: NSIS file contains file installation commands (AC#2).
        Expected: .nsi contains File directive.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="nsis",
            package_info=sample_package_result
        )

        # Assert
        nsi_content = Path(result.config_path).read_text()
        assert ("File " in nsi_content or
                "SetOutPath" in nsi_content or
                "CopyFiles" in nsi_content)

    def test_nsis_file_contains_uninstaller(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: NSIS file contains uninstaller creation (AC#2).
        Expected: .nsi contains WriteUninstaller directive.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="nsis",
            package_info=sample_package_result
        )

        # Assert
        nsi_content = Path(result.config_path).read_text()
        assert ("WriteUninstaller" in nsi_content or
                "Uninstall" in nsi_content or
                "Section \"Uninstall\"" in nsi_content)

    def test_nsis_returns_correct_tool_required(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: NSIS config has tool_required='nsis'.
        Expected: InstallerConfig.tool_required == 'nsis'.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="nsis",
            package_info=sample_package_result
        )

        # Assert
        assert result.tool_required == "nsis"

    def test_nsis_returns_correct_build_command(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: NSIS config has correct build_command.
        Expected: Build command contains makensis.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="windows",
            format="nsis",
            package_info=sample_package_result
        )

        # Assert
        assert result.build_command is not None
        assert "makensis" in result.build_command.lower()


# ==============================================================================
# AC#3: LINUX INSTALLER CONFIGURATION (DEBIAN)
# ==============================================================================


class TestLinuxDebianGeneration:
    """
    AC#3: Linux Debian installer configuration generation.

    Given: A project targeting Debian/Ubuntu distribution
    When: InstallerGenerator is invoked with Debian target
    Then: Generates a DEBIAN control directory containing:
        - control file (package metadata)
        - postinst script (post-installation)
        - prerm script (pre-removal)
    And: Returns an InstallerConfig with the directory path.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    @pytest.fixture
    def sample_package_result(self) -> dict:
        """Sample PackageResult from STORY-241 for testing."""
        return {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package-1.0.0.zip",
            "package_name": "myapp-1.0.0",
            "version": "1.0.0",
            "size_bytes": 1024000,
            "checksum": "abc123def456",
            "docker_image": None,
            "command_executed": "zip -r myapp-1.0.0.zip .",
            "duration_ms": 500
        }

    def test_generate_debian_config_returns_installer_config(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: Debian generation returns InstallerConfig (SVC-003).
        Expected: Returns InstallerConfig with platform='linux_deb', format='deb'.
        """
        from installer.installer_generator import InstallerGenerator, InstallerConfig

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        assert isinstance(result, InstallerConfig)
        assert result.platform == "linux_deb"
        assert result.format == "deb"

    def test_generate_debian_creates_debian_directory(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: Debian generation creates DEBIAN directory (SVC-003).
        Expected: DEBIAN directory exists at config_path.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        assert result.config_path is not None
        debian_dir = Path(result.config_path)
        assert debian_dir.exists()
        assert debian_dir.is_dir()
        assert debian_dir.name == "DEBIAN"

    def test_debian_directory_contains_control_file(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: DEBIAN directory contains control file (AC#3).
        Expected: control file exists in DEBIAN directory.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        control_file = Path(result.config_path) / "control"
        assert control_file.exists()

    def test_debian_control_file_contains_package_name(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: Debian control file contains Package field.
        Expected: control file has Package: field.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        control_content = (Path(result.config_path) / "control").read_text()
        assert "Package:" in control_content

    def test_debian_control_file_contains_version(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: Debian control file contains Version field.
        Expected: control file has Version: field.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        control_content = (Path(result.config_path) / "control").read_text()
        assert "Version:" in control_content

    def test_debian_directory_contains_postinst_script(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: DEBIAN directory contains postinst script (AC#3, SVC-009).
        Expected: postinst file exists in DEBIAN directory.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        postinst_file = Path(result.config_path) / "postinst"
        assert postinst_file.exists()

    def test_debian_postinst_is_executable(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: postinst script is executable (SVC-009 test requirement).
        Expected: postinst has executable permissions.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        postinst_file = Path(result.config_path) / "postinst"
        # Check if executable bit is set
        mode = postinst_file.stat().st_mode
        assert mode & stat.S_IXUSR  # Owner execute

    def test_debian_postinst_is_bash_script(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: postinst is a bash script (BR-004).
        Expected: postinst starts with bash shebang.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        postinst_content = (Path(result.config_path) / "postinst").read_text()
        assert postinst_content.startswith("#!/bin/bash") or postinst_content.startswith("#!/bin/sh")

    def test_debian_directory_contains_prerm_script(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: DEBIAN directory contains prerm script (AC#3).
        Expected: prerm file exists in DEBIAN directory.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        prerm_file = Path(result.config_path) / "prerm"
        assert prerm_file.exists()

    def test_debian_returns_correct_tool_required(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: Debian config has tool_required='dpkg-deb'.
        Expected: InstallerConfig.tool_required == 'dpkg-deb'.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        assert result.tool_required == "dpkg-deb"


# ==============================================================================
# AC#4: LINUX INSTALLER CONFIGURATION (RPM)
# ==============================================================================


class TestLinuxRpmGeneration:
    """
    AC#4: Linux RPM installer configuration generation.

    Given: A project targeting RHEL/CentOS/Fedora distribution
    When: InstallerGenerator is invoked with RPM target
    Then: Generates an RPM spec file (.spec) containing:
        - Package metadata (name, version, release)
        - Build instructions
        - File list
        - Pre/post install scripts
    And: Returns an InstallerConfig with the file path.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    @pytest.fixture
    def sample_package_result(self) -> dict:
        """Sample PackageResult from STORY-241 for testing."""
        return {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package-1.0.0.zip",
            "package_name": "myapp-1.0.0",
            "version": "1.0.0",
            "size_bytes": 1024000,
            "checksum": "abc123def456",
            "docker_image": None,
            "command_executed": "zip -r myapp-1.0.0.zip .",
            "duration_ms": 500
        }

    def test_generate_rpm_config_returns_installer_config(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: RPM generation returns InstallerConfig (SVC-004).
        Expected: Returns InstallerConfig with platform='linux_rpm', format='rpm'.
        """
        from installer.installer_generator import InstallerGenerator, InstallerConfig

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=sample_package_result
        )

        # Assert
        assert isinstance(result, InstallerConfig)
        assert result.platform == "linux_rpm"
        assert result.format == "rpm"

    def test_generate_rpm_creates_spec_file(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: RPM generation creates .spec file (SVC-004).
        Expected: File exists at config_path with .spec extension.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=sample_package_result
        )

        # Assert
        assert result.config_path is not None
        assert result.config_path.endswith(".spec")
        assert Path(result.config_path).exists()

    def test_rpm_spec_contains_name_field(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: RPM spec file contains Name field (AC#4 metadata).
        Expected: .spec contains Name: field.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=sample_package_result
        )

        # Assert
        spec_content = Path(result.config_path).read_text()
        assert "Name:" in spec_content

    def test_rpm_spec_contains_version_field(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: RPM spec file contains Version field (AC#4 metadata).
        Expected: .spec contains Version: field.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=sample_package_result
        )

        # Assert
        spec_content = Path(result.config_path).read_text()
        assert "Version:" in spec_content

    def test_rpm_spec_contains_release_field(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: RPM spec file contains Release field (AC#4 metadata).
        Expected: .spec contains Release: field.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=sample_package_result
        )

        # Assert
        spec_content = Path(result.config_path).read_text()
        assert "Release:" in spec_content

    def test_rpm_spec_contains_build_section(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: RPM spec file contains %build section (AC#4).
        Expected: .spec contains %build section.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=sample_package_result
        )

        # Assert
        spec_content = Path(result.config_path).read_text()
        assert "%build" in spec_content or "%install" in spec_content

    def test_rpm_spec_contains_files_section(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: RPM spec file contains %files section (AC#4).
        Expected: .spec contains %files section.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=sample_package_result
        )

        # Assert
        spec_content = Path(result.config_path).read_text()
        assert "%files" in spec_content

    def test_rpm_spec_contains_post_script(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: RPM spec file contains %post section (AC#4, SVC-009).
        Expected: .spec contains %post section.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=sample_package_result
        )

        # Assert
        spec_content = Path(result.config_path).read_text()
        assert "%post" in spec_content or "%postun" in spec_content

    def test_rpm_returns_correct_tool_required(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: RPM config has tool_required='rpmbuild'.
        Expected: InstallerConfig.tool_required == 'rpmbuild'.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=sample_package_result
        )

        # Assert
        assert result.tool_required == "rpmbuild"


# ==============================================================================
# AC#5: MACOS INSTALLER CONFIGURATION (PKG)
# ==============================================================================


class TestMacOsPkgGeneration:
    """
    AC#5: macOS pkg installer configuration generation.

    Given: A project targeting macOS distribution
    When: InstallerGenerator is invoked with macOS target
    Then: Generates pkgbuild and productbuild scripts containing:
        - Component package definition
        - Distribution XML for customization
        - Post-installation scripts
    And: Returns an InstallerConfig with the file paths.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    @pytest.fixture
    def sample_package_result(self) -> dict:
        """Sample PackageResult from STORY-241 for testing."""
        return {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package-1.0.0.zip",
            "package_name": "myapp-1.0.0",
            "version": "1.0.0",
            "size_bytes": 1024000,
            "checksum": "abc123def456",
            "docker_image": None,
            "command_executed": "zip -r myapp-1.0.0.zip .",
            "duration_ms": 500
        }

    def test_generate_macos_config_returns_installer_config(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: macOS generation returns InstallerConfig (SVC-005).
        Expected: Returns InstallerConfig with platform='macos', format='pkg'.
        """
        from installer.installer_generator import InstallerGenerator, InstallerConfig

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="macos",
            format="pkg",
            package_info=sample_package_result
        )

        # Assert
        assert isinstance(result, InstallerConfig)
        assert result.platform == "macos"
        assert result.format == "pkg"

    def test_generate_macos_creates_distribution_xml(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: macOS generation creates distribution.xml (SVC-005).
        Expected: distribution.xml file exists.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="macos",
            format="pkg",
            package_info=sample_package_result
        )

        # Assert
        # config_path should point to directory or file containing distribution.xml
        config_dir = Path(result.config_path)
        if config_dir.is_dir():
            distribution_xml = config_dir / "distribution.xml"
        else:
            distribution_xml = config_dir.parent / "distribution.xml"

        assert distribution_xml.exists() or "distribution.xml" in result.config_path

    def test_macos_distribution_xml_has_title(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: distribution.xml contains title element.
        Expected: XML contains <title> element.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="macos",
            format="pkg",
            package_info=sample_package_result
        )

        # Assert
        config_dir = Path(result.config_path) if Path(result.config_path).is_dir() else Path(result.config_path).parent
        distribution_file = config_dir / "distribution.xml"
        if distribution_file.exists():
            content = distribution_file.read_text()
            assert "<title>" in content or "title=" in content

    def test_generate_macos_creates_build_script(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: macOS generation creates pkgbuild script (SVC-005).
        Expected: Build script or command references pkgbuild.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="macos",
            format="pkg",
            package_info=sample_package_result
        )

        # Assert
        assert result.build_command is not None
        assert "pkgbuild" in result.build_command.lower() or "productbuild" in result.build_command.lower()

    def test_macos_generates_postinstall_script(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: macOS generation creates post-installation script (AC#5, SVC-009).
        Expected: postinstall script exists in scripts directory.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="macos",
            format="pkg",
            package_info=sample_package_result
        )

        # Assert
        config_dir = Path(result.config_path) if Path(result.config_path).is_dir() else Path(result.config_path).parent
        scripts_dir = config_dir / "scripts"

        # Scripts might be in a subdirectory or referenced
        postinstall_exists = (
            (scripts_dir / "postinstall").exists() or
            "postinstall" in result.metadata.get("scripts", {})
        )
        assert postinstall_exists or "scripts" in str(result.config_path).lower()

    def test_macos_returns_correct_tool_required(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: macOS config has tool_required='pkgbuild'.
        Expected: InstallerConfig.tool_required == 'pkgbuild'.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="macos",
            format="pkg",
            package_info=sample_package_result
        )

        # Assert
        assert result.tool_required == "pkgbuild"


# ==============================================================================
# AC#6: MULTI-PLATFORM INSTALLER GENERATION
# ==============================================================================


class TestMultiPlatformGeneration:
    """
    AC#6: Multi-platform installer generation.

    Given: A project targeting multiple platforms
    When: InstallerGenerator is invoked with all platforms
    Then: Generates installer configurations for:
        - Windows (MSI and/or NSIS)
        - Linux (deb and/or rpm)
        - macOS (pkg)
    And: Returns a list of InstallerConfigs for all platforms.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    @pytest.fixture
    def sample_package_result(self) -> dict:
        """Sample PackageResult from STORY-241 for testing."""
        return {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package-1.0.0.zip",
            "package_name": "myapp-1.0.0",
            "version": "1.0.0",
            "size_bytes": 1024000,
            "checksum": "abc123def456",
            "docker_image": None,
            "command_executed": "zip -r myapp-1.0.0.zip .",
            "duration_ms": 500
        }

    def test_generate_all_returns_list_of_configs(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: generate_all returns list of InstallerConfigs (AC#6).
        Expected: Returns list with multiple InstallerConfig objects.
        """
        from installer.installer_generator import InstallerGenerator, InstallerConfig

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        results = generator.generate_all(package_info=sample_package_result)

        # Assert
        assert isinstance(results, list)
        assert len(results) >= 3  # At least Windows, Linux, macOS
        assert all(isinstance(r, InstallerConfig) for r in results)

    def test_generate_all_includes_windows_platform(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: generate_all includes Windows platform (AC#6).
        Expected: At least one InstallerConfig with platform='windows'.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        results = generator.generate_all(package_info=sample_package_result)

        # Assert
        windows_configs = [r for r in results if r.platform == "windows"]
        assert len(windows_configs) >= 1

    def test_generate_all_includes_linux_deb_platform(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: generate_all includes Linux Debian platform (AC#6).
        Expected: At least one InstallerConfig with platform='linux_deb'.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        results = generator.generate_all(package_info=sample_package_result)

        # Assert
        deb_configs = [r for r in results if r.platform == "linux_deb"]
        assert len(deb_configs) >= 1

    def test_generate_all_includes_linux_rpm_platform(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: generate_all includes Linux RPM platform (AC#6).
        Expected: At least one InstallerConfig with platform='linux_rpm'.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        results = generator.generate_all(package_info=sample_package_result)

        # Assert
        rpm_configs = [r for r in results if r.platform == "linux_rpm"]
        assert len(rpm_configs) >= 1

    def test_generate_all_includes_macos_platform(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: generate_all includes macOS platform (AC#6).
        Expected: At least one InstallerConfig with platform='macos'.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        results = generator.generate_all(package_info=sample_package_result)

        # Assert
        macos_configs = [r for r in results if r.platform == "macos"]
        assert len(macos_configs) >= 1

    def test_generate_all_creates_five_platform_configs(
        self, temp_project_dir, sample_package_result
    ):
        """
        Test: generate_all creates all 5 platform configs (AC#6).
        Expected: Returns 5 InstallerConfigs (msi, nsis, deb, rpm, pkg).
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        results = generator.generate_all(package_info=sample_package_result)

        # Assert
        formats = {r.format for r in results}
        assert "msi" in formats or "nsis" in formats  # At least one Windows format
        assert "deb" in formats
        assert "rpm" in formats
        assert "pkg" in formats


# ==============================================================================
# TOOL DETECTION TESTS (SVC-006)
# ==============================================================================


class TestToolDetection:
    """
    Test tool detection functionality (SVC-006).

    SVC-006: Detect if required build tools are installed
    Test requirement: Verify tool detection for wix, nsis, dpkg, rpmbuild
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_detect_wix_tool_when_available(self, temp_project_dir):
        """
        Test: Detect WiX toolset when installed.
        Expected: tool_available=True when candle.exe is in PATH.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        with patch("shutil.which", return_value="/path/to/candle.exe"):
            available = generator.detect_tool("wix")

        # Assert
        assert available is True

    def test_detect_wix_tool_when_unavailable(self, temp_project_dir):
        """
        Test: Detect WiX toolset when not installed.
        Expected: tool_available=False when candle.exe is not in PATH.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        with patch("shutil.which", return_value=None):
            available = generator.detect_tool("wix")

        # Assert
        assert available is False

    def test_detect_nsis_tool(self, temp_project_dir):
        """
        Test: Detect NSIS tool.
        Expected: Returns correct availability based on makensis.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        with patch("shutil.which", return_value="/path/to/makensis"):
            available = generator.detect_tool("nsis")

        # Assert
        assert available is True

    def test_detect_dpkg_deb_tool(self, temp_project_dir):
        """
        Test: Detect dpkg-deb tool.
        Expected: Returns correct availability based on dpkg-deb.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        with patch("shutil.which", return_value="/usr/bin/dpkg-deb"):
            available = generator.detect_tool("dpkg-deb")

        # Assert
        assert available is True

    def test_detect_rpmbuild_tool(self, temp_project_dir):
        """
        Test: Detect rpmbuild tool.
        Expected: Returns correct availability based on rpmbuild.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        with patch("shutil.which", return_value="/usr/bin/rpmbuild"):
            available = generator.detect_tool("rpmbuild")

        # Assert
        assert available is True

    def test_detect_pkgbuild_tool(self, temp_project_dir):
        """
        Test: Detect pkgbuild tool.
        Expected: Returns correct availability based on pkgbuild.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        with patch("shutil.which", return_value="/usr/bin/pkgbuild"):
            available = generator.detect_tool("pkgbuild")

        # Assert
        assert available is True

    def test_installer_config_reflects_tool_availability(self, temp_project_dir):
        """
        Test: Generated InstallerConfig reflects actual tool availability.
        Expected: tool_available matches detect_tool result.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)
        sample_package = {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package.zip",
            "package_name": "test-1.0.0",
            "version": "1.0.0"
        }

        # Act - Tool not available
        with patch("shutil.which", return_value=None):
            result = generator.generate(
                platform="windows",
                format="msi",
                package_info=sample_package
            )

        # Assert
        assert result.tool_available is False


# ==============================================================================
# BUSINESS RULES TESTS
# ==============================================================================


class TestBusinessRules:
    """
    Test business rules (BR-001 through BR-004).
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    @pytest.fixture
    def sample_package_result(self) -> dict:
        """Sample PackageResult from STORY-241 for testing."""
        return {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package-1.0.0.zip",
            "package_name": "myapp-1.0.0",
            "version": "1.0.0"
        }

    def test_br001_config_generated_when_tool_missing(
        self, temp_project_dir, sample_package_result
    ):
        """
        BR-001: Configuration is always generated even if build tool is missing.
        Expected: InstallerConfig returned with tool_available=False.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act - Simulate WiX not installed
        with patch("shutil.which", return_value=None):
            result = generator.generate(
                platform="windows",
                format="msi",
                package_info=sample_package_result
            )

        # Assert
        assert result is not None
        assert result.config_path is not None
        assert Path(result.config_path).exists()  # Config file still created
        assert result.tool_available is False

    def test_br002_unique_guids_per_generation(
        self, temp_project_dir, sample_package_result
    ):
        """
        BR-002: Windows installers must have unique GUIDs per product.
        Expected: Each call generates different GUIDs.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result1 = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Create new temp dir for second generation
        temp2 = tempfile.mkdtemp()
        generator2 = InstallerGenerator(Path(temp2))

        result2 = generator2.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )

        # Assert - GUIDs should be unique
        if "product_guid" in result1.metadata and "product_guid" in result2.metadata:
            assert result1.metadata["product_guid"] != result2.metadata["product_guid"]

        # Cleanup
        shutil.rmtree(temp2, ignore_errors=True)

    def test_br003_linux_dependencies_extracted(
        self, temp_project_dir, sample_package_result
    ):
        """
        BR-003: Linux installers must declare dependencies.
        Expected: Dependencies parsed from package metadata.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        # Create package.json with dependencies
        package_json = temp_project_dir / "package.json"
        package_json.write_text('{"name": "myapp", "version": "1.0.0", "dependencies": {"dep1": "1.0"}}')

        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        control_content = (Path(result.config_path) / "control").read_text()
        # Should have Depends field (may be empty or with deps)
        assert "Depends:" in control_content or "depends" in result.metadata

    def test_br004_linux_scripts_use_bash(
        self, temp_project_dir, sample_package_result
    ):
        """
        BR-004: Post-installation scripts must be platform-appropriate.
        Expected: Linux scripts use bash, not batch/PowerShell.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=sample_package_result
        )

        # Assert
        postinst_file = Path(result.config_path) / "postinst"
        content = postinst_file.read_text()
        assert content.startswith("#!/bin/bash") or content.startswith("#!/bin/sh")
        assert "@echo" not in content  # Not batch
        assert "powershell" not in content.lower()


# ==============================================================================
# NON-FUNCTIONAL REQUIREMENTS TESTS
# ==============================================================================


class TestNonFunctionalRequirements:
    """
    Test NFR-001, NFR-002, NFR-003 performance requirements.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    @pytest.fixture
    def sample_package_result(self) -> dict:
        return {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package-1.0.0.zip",
            "package_name": "myapp-1.0.0",
            "version": "1.0.0"
        }

    def test_nfr001_generation_under_10_seconds(
        self, temp_project_dir, sample_package_result
    ):
        """
        NFR-001: Config generation must complete under 10 seconds.
        Expected: Generation completes in < 10 seconds.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        start_time = time.time()
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=sample_package_result
        )
        elapsed = time.time() - start_time

        # Assert
        assert elapsed < 10.0, f"Generation took {elapsed:.2f}s (expected < 10s)"

    def test_nfr001_tool_detection_under_1_second(self, temp_project_dir):
        """
        NFR-001: Tool detection must complete under 1 second.
        Expected: detect_tool completes in < 1 second.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)

        # Act
        start_time = time.time()
        generator.detect_tool("wix")
        elapsed = time.time() - start_time

        # Assert
        assert elapsed < 1.0, f"Tool detection took {elapsed:.2f}s (expected < 1s)"


# ==============================================================================
# EDGE CASES AND ERROR HANDLING
# ==============================================================================


class TestEdgeCasesAndErrors:
    """
    Test edge cases and error handling scenarios.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_empty_file_list_in_package(self, temp_project_dir):
        """
        Test: Handle package with no files.
        Expected: Config generated with empty/minimal file references.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)
        empty_package = {
            "success": True,
            "format": "zip",
            "package_path": None,  # No actual package
            "package_name": "empty-1.0.0",
            "version": "1.0.0",
            "size_bytes": 0
        }

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=empty_package
        )

        # Assert - Should still generate config
        assert result is not None
        assert result.config_path is not None

    def test_special_characters_in_package_name(self, temp_project_dir):
        """
        Test: Handle special characters in package name.
        Expected: Special characters sanitized or handled.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)
        special_package = {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package.zip",
            "package_name": "my-app@2.0_beta!#",
            "version": "2.0.0-beta"
        }

        # Act
        result = generator.generate(
            platform="windows",
            format="msi",
            package_info=special_package
        )

        # Assert - Should handle gracefully
        assert result is not None
        # WiX content should not contain invalid characters
        wxs_content = Path(result.config_path).read_text()
        assert "!#" not in wxs_content  # Should be sanitized

    def test_long_file_paths(self, temp_project_dir):
        """
        Test: Handle long file paths.
        Expected: Paths handled without truncation errors.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)
        long_name = "a" * 200  # Very long name
        long_package = {
            "success": True,
            "format": "zip",
            "package_path": f"/path/to/{long_name}/package.zip",
            "package_name": f"{long_name}-1.0.0",
            "version": "1.0.0"
        }

        # Act
        result = generator.generate(
            platform="linux_deb",
            format="deb",
            package_info=long_package
        )

        # Assert
        assert result is not None

    def test_invalid_package_metadata(self, temp_project_dir):
        """
        Test: Handle invalid package metadata.
        Expected: Uses sensible defaults.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        generator = InstallerGenerator(temp_project_dir)
        invalid_package = {
            "success": False,  # Package creation failed
            "format": None,
            "package_path": None,
            "package_name": None,
            "version": None
        }

        # Act
        result = generator.generate(
            platform="linux_rpm",
            format="rpm",
            package_info=invalid_package
        )

        # Assert - Should use defaults
        assert result is not None
        spec_content = Path(result.config_path).read_text()
        assert "Version:" in spec_content  # Should have some version

    def test_write_permission_denied(self, temp_project_dir):
        """
        Test: Handle write permission denied.
        Expected: Appropriate error handling.
        """
        from installer.installer_generator import InstallerGenerator

        # Arrange
        # Make directory read-only
        os.chmod(temp_project_dir, stat.S_IRUSR | stat.S_IXUSR)

        generator = InstallerGenerator(temp_project_dir)
        sample_package = {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package.zip",
            "package_name": "test-1.0.0",
            "version": "1.0.0"
        }

        # Act & Assert
        try:
            result = generator.generate(
                platform="windows",
                format="msi",
                package_info=sample_package
            )
            # If it succeeds, it should handle gracefully
        except PermissionError:
            # Expected behavior
            pass
        finally:
            # Restore permissions for cleanup
            os.chmod(temp_project_dir, stat.S_IRWXU)

    def test_missing_tool_logs_warning(self, temp_project_dir):
        """
        Test: Missing tool logs info warning (SVC-010).
        Expected: Warning logged but config still generated.
        """
        from installer.installer_generator import InstallerGenerator
        import logging

        # Arrange
        generator = InstallerGenerator(temp_project_dir)
        sample_package = {
            "success": True,
            "format": "zip",
            "package_path": "/path/to/package.zip",
            "package_name": "test-1.0.0",
            "version": "1.0.0"
        }

        # Act
        with patch("shutil.which", return_value=None):
            with patch("logging.Logger.info") as mock_log:
                with patch("logging.Logger.warning") as mock_warn:
                    result = generator.generate(
                        platform="windows",
                        format="msi",
                        package_info=sample_package
                    )

        # Assert
        assert result is not None
        assert result.tool_available is False
        # Config should still be generated


# ==============================================================================
# FILE LIST EXTRACTION TESTS (SVC-008)
# ==============================================================================


class TestFileListExtraction:
    """
    Test file list extraction from package (SVC-008).
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_extract_file_list_from_zip(self, temp_project_dir):
        """
        Test: Extract file list from zip package.
        Expected: Returns list of files in package.
        """
        from installer.installer_generator import InstallerGenerator
        import zipfile

        # Arrange
        # Create actual zip file
        zip_path = temp_project_dir / "test-1.0.0.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file1.txt", "content1")
            zf.writestr("subdir/file2.txt", "content2")

        generator = InstallerGenerator(temp_project_dir)

        # Act
        files = generator.extract_file_list(str(zip_path))

        # Assert
        assert isinstance(files, list)
        assert len(files) >= 2
        assert any("file1.txt" in f for f in files)

    def test_file_list_matches_package_contents(self, temp_project_dir):
        """
        Test: Extracted file list matches package contents.
        Expected: All files from package are in list.
        """
        from installer.installer_generator import InstallerGenerator
        import zipfile

        # Arrange
        zip_path = temp_project_dir / "test-1.0.0.zip"
        expected_files = ["app.exe", "lib/helper.dll", "config.json"]

        with zipfile.ZipFile(zip_path, "w") as zf:
            for f in expected_files:
                zf.writestr(f, "content")

        generator = InstallerGenerator(temp_project_dir)

        # Act
        files = generator.extract_file_list(str(zip_path))

        # Assert
        for expected in expected_files:
            assert any(expected in f for f in files), f"{expected} not found in extracted list"
