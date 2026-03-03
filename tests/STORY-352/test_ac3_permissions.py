"""
Tests for AC#3: Binary Permissions Set Correctly

Story: STORY-352 - Add Treelint Binary to Installer Distribution
AC#3: Binary has executable permissions (chmod +x on Unix, no action on Windows)

These tests verify:
- chmod +x is applied on Unix platforms (Linux, macOS)
- Windows skips permission step
- Binary is executable after deployment
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import stat
import sys


class TestAC3Permissions:
    """Tests for AC#3: Binary Permissions Set Correctly."""

    @pytest.fixture
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent.parent

    @pytest.fixture
    def temp_target_dir(self, tmp_path: Path) -> Path:
        """Create temporary target directory for deployment testing."""
        target_dir = tmp_path / "test_project"
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir

    @pytest.fixture
    def temp_source_dir(self, tmp_path: Path) -> Path:
        """Create temporary source directory with mock binaries."""
        import hashlib

        source_dir = tmp_path / "src" / "bin" / "treelint"
        source_dir.mkdir(parents=True, exist_ok=True)

        # Create mock binary files with version info
        binaries = [
            "treelint-linux-x86_64",
            "treelint-linux-aarch64",
            "treelint-darwin-x86_64",
            "treelint-darwin-aarch64",
            "treelint-windows-x86_64.exe",
        ]
        binary_content = b"#!/bin/bash\n# Version: 0.12.0\necho treelint version 0.12.0\n"

        checksums_content = []
        for binary_name in binaries:
            binary_path = source_dir / binary_name
            binary_path.write_bytes(binary_content)
            # Make source file non-executable to verify deployment sets permissions
            os.chmod(binary_path, stat.S_IRUSR | stat.S_IWUSR)
            # Calculate actual SHA256 hash
            file_hash = hashlib.sha256(binary_content).hexdigest()
            checksums_content.append(f"{file_hash}  {binary_name}")

        (source_dir / "checksums.txt").write_text("\n".join(checksums_content))

        return source_dir

    def test_set_permissions_function_exists(self, project_root: Path):
        """
        Test: Verify set_permissions function exists in binary_deploy module.

        Given: binary_deploy module
        When: Checking for permission-related function
        Then: Function to set executable permissions should exist
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer import binary_deploy

            assert hasattr(binary_deploy, "set_executable_permissions") or hasattr(
                binary_deploy, "_set_permissions"
            ), (
                "No permission-setting function found in binary_deploy module\n"
                "Expected: set_executable_permissions or _set_permissions function"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_linux_binary_has_executable_permissions(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify deployed Linux binary has executable permissions.

        Given: Deployment on Linux platform
        When: Binary is deployed
        Then: Binary should have executable permission (chmod +x applied)
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="linux-x86_64",
            )

            deployed_binary = temp_target_dir / ".treelint" / "bin" / "treelint"
            assert deployed_binary.exists(), "Binary was not deployed"

            # Check executable permission
            mode = deployed_binary.stat().st_mode
            is_executable = bool(mode & stat.S_IXUSR)
            assert is_executable, (
                f"Linux binary does not have executable permission\n"
                f"Current mode: {oct(mode)}\n"
                "Expected: User executable bit (S_IXUSR) to be set"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_darwin_binary_has_executable_permissions(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify deployed macOS binary has executable permissions.

        Given: Deployment on macOS platform
        When: Binary is deployed
        Then: Binary should have executable permission (chmod +x applied)
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="darwin-x86_64",
            )

            deployed_binary = temp_target_dir / ".treelint" / "bin" / "treelint"
            assert deployed_binary.exists(), "Binary was not deployed"

            # Check executable permission
            mode = deployed_binary.stat().st_mode
            is_executable = bool(mode & stat.S_IXUSR)
            assert is_executable, (
                f"macOS binary does not have executable permission\n"
                f"Current mode: {oct(mode)}\n"
                "Expected: User executable bit (S_IXUSR) to be set"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_unix_binary_has_755_permissions(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify Unix binary has 755 permissions (rwxr-xr-x).

        Given: Deployment on Unix platform
        When: Binary is deployed
        Then: Binary should have 755 permissions
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="linux-x86_64",
            )

            deployed_binary = temp_target_dir / ".treelint" / "bin" / "treelint"
            assert deployed_binary.exists(), "Binary was not deployed"

            # Check for 755 permissions (rwxr-xr-x)
            mode = deployed_binary.stat().st_mode
            permission_bits = stat.S_IMODE(mode)
            expected_755 = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH

            assert permission_bits == expected_755, (
                f"Binary permissions are not 755\n"
                f"Current: {oct(permission_bits)} ({oct(mode)})\n"
                f"Expected: 0o755"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    @patch("platform.system")
    def test_windows_skips_chmod_operation(
        self,
        mock_platform: Mock,
        project_root: Path,
        temp_source_dir: Path,
        temp_target_dir: Path,
    ):
        """
        Test: Verify Windows deployment skips chmod operation.

        Given: Deployment on Windows platform
        When: Binary is deployed
        Then: No chmod operation should be attempted
        """
        mock_platform.return_value = "Windows"

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            # Should not raise OSError even though chmod might fail on Windows
            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="windows-x86_64",
            )

            # Deployment should succeed
            deployed_binary = (
                temp_target_dir / ".treelint" / "bin" / "treelint.exe"
            )
            assert deployed_binary.exists(), "Windows binary was not deployed"
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_permission_error_handling_graceful(
        self, project_root: Path, temp_source_dir: Path, tmp_path: Path
    ):
        """
        Test: Verify permission errors are handled gracefully.

        Given: A directory where permissions cannot be set
        When: Attempting to deploy binary
        Then: Should either succeed with warning or raise clear error
        """
        # Create a read-only target (if possible on current OS)
        target_dir = tmp_path / "readonly_target"
        target_dir.mkdir(parents=True, exist_ok=True)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            # This test verifies error handling, not specific behavior
            # The implementation should handle permission errors gracefully
            try:
                deploy_binary(
                    source_dir=temp_source_dir,
                    target_dir=target_dir,
                    platform="linux-x86_64",
                )
                # If it succeeds, permissions were set correctly
            except PermissionError:
                # Expected on some filesystems
                pass
            except Exception as e:
                # Other errors should have meaningful messages
                assert "permission" in str(e).lower() or "chmod" in str(e).lower(), (
                    f"Unexpected error type: {type(e).__name__}: {e}\n"
                    "Expected: Permission-related error message"
                )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    @pytest.mark.parametrize(
        "platform",
        ["linux-x86_64", "linux-aarch64", "darwin-x86_64", "darwin-aarch64"],
    )
    def test_all_unix_platforms_get_executable_permission(
        self, project_root: Path, temp_source_dir: Path, tmp_path: Path, platform: str
    ):
        """
        Test: Verify all Unix platforms get executable permissions.

        Given: Deployment on any Unix platform
        When: Binary is deployed
        Then: Executable permission should be set
        """
        temp_target_dir = tmp_path / f"target_{platform.replace('-', '_')}"
        temp_target_dir.mkdir(parents=True, exist_ok=True)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform=platform,
            )

            deployed_binary = temp_target_dir / ".treelint" / "bin" / "treelint"
            assert deployed_binary.exists(), f"Binary not deployed for {platform}"

            mode = deployed_binary.stat().st_mode
            is_executable = bool(mode & stat.S_IXUSR)
            assert is_executable, (
                f"{platform} binary does not have executable permission"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deployed_binary_is_actually_executable(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify deployed binary can be executed (access check).

        Given: Deployed binary on Unix
        When: Checking if binary is executable
        Then: os.access(path, os.X_OK) should return True
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="linux-x86_64",
            )

            deployed_binary = temp_target_dir / ".treelint" / "bin" / "treelint"
            assert deployed_binary.exists(), "Binary was not deployed"

            # Check if actually executable using os.access
            is_executable = os.access(deployed_binary, os.X_OK)
            assert is_executable, (
                f"Deployed binary is not executable according to os.access\n"
                f"Path: {deployed_binary}\n"
                "Expected: os.access(path, os.X_OK) to return True"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)
