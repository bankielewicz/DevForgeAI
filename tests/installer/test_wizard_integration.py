"""
Integration tests for wizard installer post-installation validation (STORY-252 AC#5).

Tests end-to-end wizard flow to verify framework files are deployed correctly:
- .claude/ directory exists after wizard completes
- devforgeai/ directory exists after wizard completes
- CLAUDE.md file exists after wizard completes

**Test Strategy:**
These tests use pytest's tmp_path fixture for isolated test directories and mock
the deploy.deploy_framework_files() function to return success while creating
expected directories. This verifies the integration chain works correctly.

**Coverage Target:** 85%+ (Integration Tests)

**Acceptance Criteria Covered:**
- AC#5: Post-Installation Validation
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import os

from installer.wizard import WizardInstaller
from installer import deploy


@pytest.fixture
def temp_install_dir(tmp_path):
    """
    Create a temporary installation directory for integration tests.

    Returns:
        Path: Temporary directory that is writable and exists.
    """
    install_dir = tmp_path / "wizard_install_target"
    install_dir.mkdir(exist_ok=True)
    return install_dir


@pytest.fixture
def mock_deploy_success(temp_install_dir):
    """
    Mock deploy.deploy_framework_files to return success and create expected directories.

    This fixture creates the expected framework structure in the target directory
    when deploy_framework_files is called, simulating a successful deployment.

    Args:
        temp_install_dir: The temporary installation directory.

    Yields:
        MagicMock: The mock deploy function for assertions.
    """
    def create_framework_structure(source_root, target_root, preserve_configs=True):
        """Side effect function that creates framework directories."""
        target = Path(target_root)

        # Create .claude/ directory structure
        claude_dir = target / ".claude"
        claude_dir.mkdir(exist_ok=True)
        (claude_dir / "skills").mkdir(exist_ok=True)
        (claude_dir / "agents").mkdir(exist_ok=True)
        (claude_dir / "commands").mkdir(exist_ok=True)

        # Create devforgeai/ directory structure
        devforgeai_dir = target / "devforgeai"
        devforgeai_dir.mkdir(exist_ok=True)
        (devforgeai_dir / "protocols").mkdir(exist_ok=True)
        (devforgeai_dir / "specs").mkdir(exist_ok=True)
        (devforgeai_dir / "specs" / "context").mkdir(parents=True, exist_ok=True)

        # Create CLAUDE.md file
        claude_md = target / "CLAUDE.md"
        claude_md.write_text("# DevForgeAI\n\nFramework configuration file.\n")

        return {
            "status": "success",
            "files_deployed": 450,
            "files_skipped": 10,
            "directories_created": 25,
            "errors": [],
        }

    with patch.object(deploy, "deploy_framework_files", side_effect=create_framework_structure) as mock:
        yield mock


@pytest.fixture
def wizard_with_mock_deploy(temp_install_dir, mock_deploy_success):
    """
    Create a WizardInstaller instance with mocked deploy function.

    Args:
        temp_install_dir: The temporary installation directory.
        mock_deploy_success: The mock deploy function fixture.

    Returns:
        tuple: (WizardInstaller instance, target path, mock deploy function)
    """
    wizard = WizardInstaller(target_path=temp_install_dir, tty_mode=False)
    return wizard, temp_install_dir, mock_deploy_success


class TestWizardIntegrationPostInstallation:
    """
    Integration tests for AC#5: Post-Installation Validation.

    Tests verify that after the wizard completes file deployment successfully,
    the target directory contains all required framework files.
    """

    def test_wizard_creates_claude_directory(self, wizard_with_mock_deploy):
        """
        Test that .claude/ directory exists after wizard completes.

        Given: The wizard completes file deployment successfully
        When: The installation finishes
        Then: The .claude/ directory exists in target

        Verification: .claude/ directory exists with subdirectories
        """
        wizard, target, mock_deploy = wizard_with_mock_deploy

        # Execute the file installation step
        result = wizard._execute_file_installation()

        # Verify deploy was called
        mock_deploy.assert_called_once()

        # Verify result indicates success
        assert result is True, "Installation should succeed"

        # Verify .claude/ directory exists
        claude_dir = target / ".claude"
        assert claude_dir.exists(), ".claude/ directory should exist after installation"
        assert claude_dir.is_dir(), ".claude/ should be a directory"

    def test_wizard_creates_claude_subdirectories(self, wizard_with_mock_deploy):
        """
        Test that .claude/ contains expected subdirectories.

        Given: The wizard completes file deployment successfully
        When: The installation finishes
        Then: The .claude/ directory contains skills, agents, commands subdirectories

        Verification: .claude/skills/, .claude/agents/, .claude/commands/ exist
        """
        wizard, target, mock_deploy = wizard_with_mock_deploy

        # Execute the file installation step
        result = wizard._execute_file_installation()

        # Verify subdirectories exist
        claude_dir = target / ".claude"
        assert (claude_dir / "skills").exists(), ".claude/skills/ should exist"
        assert (claude_dir / "agents").exists(), ".claude/agents/ should exist"
        assert (claude_dir / "commands").exists(), ".claude/commands/ should exist"

    def test_wizard_creates_devforgeai_directory(self, wizard_with_mock_deploy):
        """
        Test that devforgeai/ directory exists after wizard completes.

        Given: The wizard completes file deployment successfully
        When: The installation finishes
        Then: The devforgeai/ directory exists in target

        Verification: devforgeai/ directory exists with subdirectories
        """
        wizard, target, mock_deploy = wizard_with_mock_deploy

        # Execute the file installation step
        result = wizard._execute_file_installation()

        # Verify deploy was called
        mock_deploy.assert_called_once()

        # Verify result indicates success
        assert result is True, "Installation should succeed"

        # Verify devforgeai/ directory exists
        devforgeai_dir = target / "devforgeai"
        assert devforgeai_dir.exists(), "devforgeai/ directory should exist after installation"
        assert devforgeai_dir.is_dir(), "devforgeai/ should be a directory"

    def test_wizard_creates_devforgeai_subdirectories(self, wizard_with_mock_deploy):
        """
        Test that devforgeai/ contains expected subdirectories.

        Given: The wizard completes file deployment successfully
        When: The installation finishes
        Then: The devforgeai/ directory contains protocols, specs/context subdirectories

        Verification: devforgeai/protocols/, devforgeai/specs/context/ exist
        """
        wizard, target, mock_deploy = wizard_with_mock_deploy

        # Execute the file installation step
        result = wizard._execute_file_installation()

        # Verify subdirectories exist
        devforgeai_dir = target / "devforgeai"
        assert (devforgeai_dir / "protocols").exists(), "devforgeai/protocols/ should exist"
        assert (devforgeai_dir / "specs").exists(), "devforgeai/specs/ should exist"
        assert (devforgeai_dir / "specs" / "context").exists(), "devforgeai/specs/context/ should exist"

    def test_wizard_creates_claude_md_file(self, wizard_with_mock_deploy):
        """
        Test that CLAUDE.md file exists after wizard completes.

        Given: The wizard completes file deployment successfully
        When: The installation finishes
        Then: CLAUDE.md file exists in target root

        Verification: CLAUDE.md file exists and is readable
        """
        wizard, target, mock_deploy = wizard_with_mock_deploy

        # Execute the file installation step
        result = wizard._execute_file_installation()

        # Verify deploy was called
        mock_deploy.assert_called_once()

        # Verify result indicates success
        assert result is True, "Installation should succeed"

        # Verify CLAUDE.md exists
        claude_md = target / "CLAUDE.md"
        assert claude_md.exists(), "CLAUDE.md should exist after installation"
        assert claude_md.is_file(), "CLAUDE.md should be a file"

    def test_wizard_claude_md_has_content(self, wizard_with_mock_deploy):
        """
        Test that CLAUDE.md file has content after wizard completes.

        Given: The wizard completes file deployment successfully
        When: The installation finishes
        Then: CLAUDE.md file contains DevForgeAI configuration

        Verification: CLAUDE.md file is not empty and contains expected content
        """
        wizard, target, mock_deploy = wizard_with_mock_deploy

        # Execute the file installation step
        result = wizard._execute_file_installation()

        # Read CLAUDE.md content
        claude_md = target / "CLAUDE.md"
        content = claude_md.read_text()

        # Verify content
        assert len(content) > 0, "CLAUDE.md should not be empty"
        assert "DevForgeAI" in content, "CLAUDE.md should contain DevForgeAI reference"


class TestWizardIntegrationFullFlow:
    """
    Integration tests for full wizard flow (step_install() method).

    Tests verify the complete installation flow through step_install(),
    which calls _do_install() which calls _execute_file_installation().
    """

    def test_step_install_creates_all_framework_files(self, wizard_with_mock_deploy):
        """
        Test complete step_install() flow creates all framework files.

        Given: Wizard is initialized with target path
        When: step_install() is called
        Then: All framework files are created (.claude/, devforgeai/, CLAUDE.md)

        Note: This test exercises the full integration chain.
        """
        wizard, target, mock_deploy = wizard_with_mock_deploy

        # Execute step_install() (which calls _do_install -> _execute_file_installation)
        result = wizard.step_install()

        # Verify result
        assert result is True, "step_install() should succeed"

        # Verify all framework components exist
        assert (target / ".claude").exists(), ".claude/ should exist"
        assert (target / "devforgeai").exists(), "devforgeai/ should exist"
        assert (target / "CLAUDE.md").exists(), "CLAUDE.md should exist"

    def test_step_install_passes_correct_target_to_deploy(self, wizard_with_mock_deploy):
        """
        Test that step_install() passes correct target path to deploy.

        Given: Wizard is initialized with specific target path
        When: step_install() is called
        Then: deploy.deploy_framework_files() receives correct target_root
        """
        wizard, target, mock_deploy = wizard_with_mock_deploy

        # Execute step_install()
        wizard.step_install()

        # Verify deploy was called with correct target
        call_args = mock_deploy.call_args
        assert call_args is not None, "deploy should be called"

        # Extract target_root from call (second positional arg)
        if len(call_args.args) >= 2:
            passed_target = call_args.args[1]
        else:
            passed_target = call_args.kwargs.get("target_root")

        assert passed_target == target, f"Target path should be {target}, got {passed_target}"


class TestWizardIntegrationDeployFailure:
    """
    Integration tests for deployment failure scenarios.

    Tests verify proper handling when deploy.deploy_framework_files() fails.
    """

    def test_wizard_handles_deploy_failure(self, temp_install_dir):
        """
        Test that wizard handles deploy failure gracefully.

        Given: deploy.deploy_framework_files() returns failure status
        When: step_install() is called
        Then: Installation returns False
        """
        wizard = WizardInstaller(target_path=temp_install_dir, tty_mode=False)

        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "failed",
                "files_deployed": 0,
                "errors": ["Permission denied"],
            }

            result = wizard._execute_file_installation()

            assert result is False, "Should return False on deployment failure"

    def test_wizard_handles_permission_error(self, temp_install_dir):
        """
        Test that wizard handles PermissionError from deploy.

        Given: deploy.deploy_framework_files() raises PermissionError
        When: _execute_file_installation() is called
        Then: Method returns False without raising
        """
        wizard = WizardInstaller(target_path=temp_install_dir, tty_mode=False)

        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.side_effect = PermissionError("Access denied")

            result = wizard._execute_file_installation()

            assert result is False, "Should return False on PermissionError"

    def test_wizard_handles_os_error(self, temp_install_dir):
        """
        Test that wizard handles OSError from deploy.

        Given: deploy.deploy_framework_files() raises OSError
        When: _execute_file_installation() is called
        Then: Method returns False without raising
        """
        wizard = WizardInstaller(target_path=temp_install_dir, tty_mode=False)

        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.side_effect = OSError(28, "No space left on device")

            result = wizard._execute_file_installation()

            assert result is False, "Should return False on OSError"


class TestWizardIntegrationSourcePath:
    """
    Integration tests for source path resolution in deployment chain.

    Tests verify that the wizard correctly resolves source path relative
    to module location and passes it to deploy function.
    """

    def test_source_path_is_path_object(self, wizard_with_mock_deploy):
        """
        Test that source path passed to deploy is a Path object.

        Given: Wizard is executing file installation
        When: deploy.deploy_framework_files() is called
        Then: source_root parameter is a Path instance
        """
        wizard, target, mock_deploy = wizard_with_mock_deploy

        wizard._execute_file_installation()

        call_args = mock_deploy.call_args
        assert call_args is not None

        # First positional arg is source_root
        source_root = call_args.args[0] if call_args.args else call_args.kwargs.get("source_root")
        assert isinstance(source_root, Path), "source_root should be a Path"

    def test_source_path_derived_from_module_location(self, wizard_with_mock_deploy):
        """
        Test that source path is derived from wizard module location.

        Given: Wizard module is at installer/wizard.py
        When: Source path is resolved
        Then: Path is relative to module location (../src/)
        """
        import installer.wizard as wizard_module

        wizard, target, mock_deploy = wizard_with_mock_deploy

        wizard._execute_file_installation()

        call_args = mock_deploy.call_args
        source_root = call_args.args[0] if call_args.args else call_args.kwargs.get("source_root")

        # Source should be <project_root>/src/
        # wizard.py is at <project_root>/installer/wizard.py
        # so source_root should be <project_root>/src/
        wizard_file = Path(wizard_module.__file__)
        expected_src = wizard_file.parent.parent / "src"

        assert source_root == expected_src, f"Source root should be {expected_src}, got {source_root}"


# ============================================================================
# Test Summary for AC#5: Post-Installation Validation
# ============================================================================
#
# These integration tests verify:
# 1. .claude/ directory exists after wizard completes
# 2. devforgeai/ directory exists after wizard completes
# 3. CLAUDE.md file exists after wizard completes
#
# The tests mock deploy.deploy_framework_files() to simulate successful
# deployment while creating the expected directory structure. This verifies
# the integration chain without requiring actual framework source files.
#
# Run with: pytest tests/installer/test_wizard_integration.py -v
# ============================================================================
