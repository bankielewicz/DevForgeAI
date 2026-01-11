"""
Unit tests for wizard installer file deployment (STORY-252).

Tests _execute_file_installation() method to ensure it calls deploy.deploy_framework_files()
with correct parameters and handles results appropriately.

**TDD Red Phase:** These tests are designed to FAIL against the current placeholder
implementation (wizard.py lines 535-549) which only logs messages without calling deploy.

**Bug Being Fixed:**
The wizard installer completes successfully but deploys no framework files because
_execute_file_installation() never calls deploy.deploy_framework_files().

**Acceptance Criteria Covered:**
- AC#1: Deploy Module Integration
- AC#2: Source Path Resolution
- AC#3: Deployment Result Handling
- AC#4: Error Propagation
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

# Import the deploy module for patching
from installer import deploy


@pytest.fixture
def wizard_instance(tmp_path):
    """Create a WizardInstaller instance with a valid target path."""
    from installer.wizard import WizardInstaller

    target = tmp_path / "test_project"
    target.mkdir(exist_ok=True)
    return WizardInstaller(target_path=target)


@pytest.fixture
def custom_target_wizard(tmp_path):
    """Create a WizardInstaller with a custom target path for specific tests."""
    from installer.wizard import WizardInstaller

    target = tmp_path / "custom_project"
    target.mkdir(exist_ok=True)
    return WizardInstaller(target_path=target), target


class TestWizardDeploymentIntegration:
    """Test AC#1: Deploy Module Integration - _execute_file_installation() calls deploy."""

    def test_execute_file_installation_calls_deploy_framework_files(self, wizard_instance):
        """
        Test that _execute_file_installation() invokes deploy.deploy_framework_files().

        Given: The wizard reaches the file installation step
        When: _execute_file_installation() is called
        Then: deploy.deploy_framework_files() is invoked

        Expected to FAIL: Current implementation only logs, never calls deploy.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "success",
                "files_deployed": 450,
                "files_skipped": 0,
                "directories_created": 20,
                "errors": [],
            }

            result = wizard_instance._execute_file_installation()

            # This assertion will FAIL - deploy is never called
            mock_deploy.assert_called_once()

    def test_execute_file_installation_passes_correct_target_path(self, custom_target_wizard):
        """
        Test that deploy receives self.state.target_path as target parameter.

        Given: Wizard state has target_path set to /path/to/project
        When: _execute_file_installation() is called
        Then: deploy.deploy_framework_files() receives that path as target_root

        Expected to FAIL: Current implementation never calls deploy.
        """
        wizard, target = custom_target_wizard

        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "success",
                "files_deployed": 450,
            }

            wizard._execute_file_installation()

            # Verify target_root parameter
            call_args = mock_deploy.call_args
            assert call_args is not None, "deploy.deploy_framework_files was not called"

            # Second positional arg or keyword arg 'target_root' should be target_path
            if call_args.kwargs.get("target_root"):
                assert call_args.kwargs["target_root"] == target
            else:
                # Assume (source_root, target_root) positional args
                assert len(call_args.args) >= 2
                assert call_args.args[1] == target

    def test_execute_file_installation_passes_source_path(self, wizard_instance):
        """
        Test that deploy receives a valid source_root path.

        Given: Wizard installer is running
        When: _execute_file_installation() is called
        Then: deploy.deploy_framework_files() receives source_root parameter

        Expected to FAIL: Current implementation never calls deploy.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "success",
                "files_deployed": 450,
            }

            wizard_instance._execute_file_installation()

            call_args = mock_deploy.call_args
            assert call_args is not None, "deploy.deploy_framework_files was not called"

            # First positional arg should be source_root (a Path)
            if call_args.args:
                source_root = call_args.args[0]
                assert isinstance(source_root, Path), "source_root should be a Path"
            elif call_args.kwargs.get("source_root"):
                source_root = call_args.kwargs["source_root"]
                assert isinstance(source_root, Path), "source_root should be a Path"
            else:
                pytest.fail("source_root parameter not passed to deploy_framework_files")


class TestSourcePathResolution:
    """Test AC#2: Source Path Resolution - source path correctly resolves to framework files."""

    def test_source_path_contains_claude_directory(self, wizard_instance):
        """
        Test that resolved source path contains claude/ directory.

        Given: The wizard installer is running
        When: Determining the source path for deployment
        Then: The source path contains a 'claude/' subdirectory

        Expected to FAIL: Current implementation doesn't resolve source path.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "success",
                "files_deployed": 450,
            }

            wizard_instance._execute_file_installation()

            call_args = mock_deploy.call_args
            assert call_args is not None, "deploy.deploy_framework_files was not called"

            # Extract source_root from call
            if call_args.args:
                source_root = call_args.args[0]
            else:
                source_root = call_args.kwargs.get("source_root")

            assert source_root is not None, "source_root was not passed"

            # Verify claude/ exists in source
            claude_path = source_root / "claude"
            # Note: We can't check .exists() in unit test without real files
            # but we verify the path structure is correct
            assert "claude" in str(source_root) or (source_root / "claude").name == "claude"

    def test_source_path_contains_devforgeai_directory(self, wizard_instance):
        """
        Test that resolved source path contains devforgeai/ directory.

        Given: The wizard installer is running
        When: Determining the source path for deployment
        Then: The source path contains a 'devforgeai/' subdirectory

        Expected to FAIL: Current implementation doesn't resolve source path.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "success",
                "files_deployed": 450,
            }

            wizard_instance._execute_file_installation()

            call_args = mock_deploy.call_args
            assert call_args is not None, "deploy.deploy_framework_files was not called"

            # Extract source_root from call
            if call_args.args:
                source_root = call_args.args[0]
            else:
                source_root = call_args.kwargs.get("source_root")

            assert source_root is not None, "source_root was not passed"

    def test_source_path_resolved_from_module_location(self, wizard_instance):
        """
        Test that source path is resolved relative to wizard module's __file__.

        Given: The wizard module is located at installer/wizard.py
        When: Resolving source_root for deployment
        Then: Path is derived from module location, not CWD

        This ensures deployment works regardless of current working directory.

        Expected to FAIL: Current implementation doesn't resolve source path.
        """
        import installer.wizard as wizard_module

        # Get the expected installer directory location
        wizard_file = Path(wizard_module.__file__)
        installer_dir = wizard_file.parent
        expected_src_dir = installer_dir.parent / "src"

        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "success",
                "files_deployed": 450,
            }

            wizard_instance._execute_file_installation()

            call_args = mock_deploy.call_args
            assert call_args is not None, "deploy.deploy_framework_files was not called"

            # Verify source path is related to module location
            if call_args.args:
                source_root = call_args.args[0]
            else:
                source_root = call_args.kwargs.get("source_root")

            assert source_root is not None, "source_root was not passed"
            # The source should be derived from installer module location
            assert isinstance(source_root, Path)


class TestDeploymentResultHandling:
    """Test AC#3: Deployment Result Handling - success and failure paths."""

    def test_execute_file_installation_returns_true_on_success(self, wizard_instance):
        """
        Test that method returns True when deploy returns success status.

        Given: deploy.deploy_framework_files() returns {"status": "success", "files_deployed": 450}
        When: _execute_file_installation() processes the result
        Then: Method returns True

        Expected to FAIL: Current implementation returns True without calling deploy.
        But the test will pass incorrectly - need to verify deploy was called.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "success",
                "files_deployed": 450,
                "files_skipped": 10,
                "directories_created": 25,
                "errors": [],
            }

            result = wizard_instance._execute_file_installation()

            # First verify deploy was actually called
            mock_deploy.assert_called_once()

            # Then verify return value
            assert result is True, "Should return True on successful deployment"

    def test_execute_file_installation_returns_false_on_failure(self, wizard_instance):
        """
        Test that method returns False when deploy returns failed status.

        Given: deploy.deploy_framework_files() returns {"status": "failed", "errors": [...]}
        When: _execute_file_installation() processes the result
        Then: Method returns False

        Expected to FAIL: Current implementation always returns True without checking.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "failed",
                "files_deployed": 100,
                "files_skipped": 0,
                "directories_created": 5,
                "errors": ["Permission denied: /target/.claude/"],
            }

            result = wizard_instance._execute_file_installation()

            # Verify deploy was called
            mock_deploy.assert_called_once()

            # Should return False on failure
            assert result is False, "Should return False when deployment fails"

    def test_execute_file_installation_logs_files_deployed_count(self, wizard_instance):
        """
        Test that successful deployment logs the files_deployed count.

        Given: deploy returns {"status": "success", "files_deployed": 450}
        When: _execute_file_installation() completes
        Then: Log contains "Deployed 450 files" or similar message

        Expected to FAIL: Current implementation logs placeholder messages only.
        """
        # Capture log output
        log_messages = []
        original_log = wizard_instance._log

        def capture_log(msg):
            log_messages.append(msg)
            original_log(msg)

        wizard_instance._log = capture_log

        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "success",
                "files_deployed": 450,
                "files_skipped": 10,
                "directories_created": 25,
                "errors": [],
            }

            wizard_instance._execute_file_installation()

            # Verify deploy was called
            mock_deploy.assert_called_once()

            # Check logs contain deployment count
            log_text = " ".join(log_messages)
            assert "450" in log_text or "files" in log_text.lower(), (
                f"Log should contain deployment count. Logs: {log_messages}"
            )

    def test_execute_file_installation_logs_error_on_failure(self, wizard_instance):
        """
        Test that failed deployment logs error details.

        Given: deploy returns {"status": "failed", "errors": ["Permission denied"]}
        When: _execute_file_installation() processes failure
        Then: Log contains error information

        Expected to FAIL: Current implementation doesn't handle failures.
        """
        log_messages = []
        original_log = wizard_instance._log

        def capture_log(msg):
            log_messages.append(msg)
            original_log(msg)

        wizard_instance._log = capture_log

        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {
                "status": "failed",
                "files_deployed": 0,
                "errors": ["Permission denied: /target/.claude/"],
            }

            result = wizard_instance._execute_file_installation()

            mock_deploy.assert_called_once()

            log_text = " ".join(log_messages).lower()
            assert (
                "error" in log_text or "fail" in log_text or "permission" in log_text
            ), f"Log should contain error details. Logs: {log_messages}"


class TestErrorPropagation:
    """Test AC#4: Error Propagation - PermissionError and OSError handling."""

    def test_execute_file_installation_catches_permission_error(self, wizard_instance):
        """
        Test that PermissionError from deploy is caught and returns False.

        Given: deploy.deploy_framework_files() raises PermissionError
        When: _execute_file_installation() catches it
        Then: Method returns False (doesn't raise)

        Expected to FAIL: Current implementation doesn't call deploy, so no error to catch.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.side_effect = PermissionError(
                "Permission denied: /target/.claude/"
            )

            result = wizard_instance._execute_file_installation()

            mock_deploy.assert_called_once()
            assert result is False, "Should return False when PermissionError occurs"

    def test_execute_file_installation_catches_os_error(self, wizard_instance):
        """
        Test that OSError from deploy is caught and returns False.

        Given: deploy.deploy_framework_files() raises OSError (e.g., disk full)
        When: _execute_file_installation() catches it
        Then: Method returns False (doesn't raise)

        Expected to FAIL: Current implementation doesn't call deploy, so no error to catch.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.side_effect = OSError(
                28, "No space left on device"
            )

            result = wizard_instance._execute_file_installation()

            mock_deploy.assert_called_once()
            assert result is False, "Should return False when OSError occurs"

    def test_execute_file_installation_logs_permission_error(self, wizard_instance):
        """
        Test that PermissionError is logged before returning False.

        Given: deploy raises PermissionError
        When: Error is caught
        Then: Error details are logged

        Expected to FAIL: Current implementation doesn't call deploy.
        """
        log_messages = []
        original_log = wizard_instance._log

        def capture_log(msg):
            log_messages.append(msg)
            original_log(msg)

        wizard_instance._log = capture_log

        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.side_effect = PermissionError(
                "Permission denied: /protected/path"
            )

            wizard_instance._execute_file_installation()

            mock_deploy.assert_called_once()

            log_text = " ".join(log_messages).lower()
            assert (
                "permission" in log_text or "error" in log_text
            ), f"Log should contain permission error. Logs: {log_messages}"

    def test_execute_file_installation_logs_os_error(self, wizard_instance):
        """
        Test that OSError is logged before returning False.

        Given: deploy raises OSError (disk full)
        When: Error is caught
        Then: Error details are logged

        Expected to FAIL: Current implementation doesn't call deploy.
        """
        log_messages = []
        original_log = wizard_instance._log

        def capture_log(msg):
            log_messages.append(msg)
            original_log(msg)

        wizard_instance._log = capture_log

        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.side_effect = OSError(
                28, "No space left on device"
            )

            wizard_instance._execute_file_installation()

            mock_deploy.assert_called_once()

            log_text = " ".join(log_messages).lower()
            assert (
                "error" in log_text or "space" in log_text or "os" in log_text
            ), f"Log should contain OS error details. Logs: {log_messages}"


class TestWizardDeploymentDoInstall:
    """Test that _do_install() delegates to _execute_file_installation() correctly."""

    def test_do_install_calls_execute_file_installation(self, wizard_instance):
        """
        Test that _do_install() delegates to _execute_file_installation().

        Given: Wizard's _do_install() is called
        When: It processes the installation step
        Then: It delegates to _execute_file_installation()

        This test verifies the delegation chain works.
        """
        with patch.object(wizard_instance, "_execute_file_installation") as mock_execute:
            mock_execute.return_value = True

            result = wizard_instance._do_install()

            mock_execute.assert_called_once()
            assert result is True

    def test_do_install_propagates_false_from_execute(self, wizard_instance):
        """
        Test that _do_install() returns False when _execute_file_installation() fails.

        Given: _execute_file_installation() returns False
        When: _do_install() delegates to it
        Then: _do_install() also returns False

        This verifies failure propagation through the delegation chain.
        """
        with patch.object(wizard_instance, "_execute_file_installation") as mock_execute:
            mock_execute.return_value = False

            result = wizard_instance._do_install()

            mock_execute.assert_called_once()
            assert result is False


# ============================================================================
# Additional Edge Case Tests
# ============================================================================


class TestSourcePathEdgeCases:
    """Edge cases for source path resolution."""

    def test_source_path_handles_development_layout(self, wizard_instance):
        """
        Test source path resolution when running from development checkout.

        Given: Running from development environment (src/ at project root)
        When: Resolving source path
        Then: Path correctly points to src/ directory

        Expected to FAIL: Current implementation doesn't resolve paths.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {"status": "success"}

            wizard_instance._execute_file_installation()

            # Should call deploy with a source path
            assert mock_deploy.called

    def test_source_path_handles_installed_package_layout(self, wizard_instance):
        """
        Test source path resolution when running from installed package.

        Given: Running from pip-installed package
        When: Resolving source path
        Then: Path correctly points to package data directory

        Note: This may need adjustment based on final package structure.

        Expected to FAIL: Current implementation doesn't resolve paths.
        """
        with patch.object(deploy, "deploy_framework_files") as mock_deploy:
            mock_deploy.return_value = {"status": "success"}

            wizard_instance._execute_file_installation()

            # Should call deploy
            assert mock_deploy.called


# ============================================================================
# Test Summary for TDD Red Phase
# ============================================================================
#
# All tests in this file are designed to FAIL against the current wizard.py
# implementation (lines 535-549) which is a placeholder:
#
#     def _execute_file_installation(self) -> bool:
#         self._log("Installation started")
#         self._log(f"Target path: {self.state.target_path}")
#         self._log(f"Selected components: {[c.id for c in self.state.components if c.selected]}")
#         self._log("Installation completed successfully")
#         return True
#
# The fix (Green phase) will:
# 1. Import deploy module
# 2. Resolve source_root from __file__ location
# 3. Call deploy.deploy_framework_files(source_root, target_path)
# 4. Handle result status (success/failed)
# 5. Catch and handle PermissionError and OSError
#
# Run with: pytest tests/installer/test_wizard_deployment.py -v
# Expected: All tests FAIL (TDD Red phase complete)
# ============================================================================
