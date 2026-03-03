"""
Tests for AC#2: Installer Deploys Binary to Appropriate Location

Story: STORY-352 - Add Treelint Binary to Installer Distribution
AC#2: The platform-appropriate treelint binary is deployed to .treelint/bin/

These tests verify:
- binary_deploy.py module exists
- Platform detection logic works correctly
- Deployment to .treelint/bin/treelint (or .treelint/bin/treelint.exe on Windows)
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
import sys


class TestAC2InstallerDeploy:
    """Tests for AC#2: Installer Deploys Binary to Appropriate Location."""

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
            # Calculate actual SHA256 hash
            file_hash = hashlib.sha256(binary_content).hexdigest()
            checksums_content.append(f"{file_hash}  {binary_name}")

        (source_dir / "checksums.txt").write_text("\n".join(checksums_content))

        return source_dir

    def test_binary_deploy_module_exists(self, project_root: Path):
        """
        Test: Verify installer/binary_deploy.py module exists.

        Given: The installer package
        When: Checking for binary deployment module
        Then: installer/binary_deploy.py should exist
        """
        binary_deploy_path = project_root / "installer" / "binary_deploy.py"
        assert binary_deploy_path.exists(), (
            f"binary_deploy.py module not found: {binary_deploy_path}\n"
            "Expected: installer/binary_deploy.py to be created"
        )

    def test_binary_deploy_module_importable(self, project_root: Path):
        """
        Test: Verify binary_deploy module can be imported.

        Given: installer/binary_deploy.py exists
        When: Attempting to import the module
        Then: Import should succeed without errors
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer import binary_deploy  # noqa: F401
        except ImportError as e:
            pytest.fail(
                f"Failed to import binary_deploy module: {e}\n"
                "Expected: Module should be importable"
            )
        finally:
            sys.path.pop(0)

    def test_deploy_binary_function_exists(self, project_root: Path):
        """
        Test: Verify deploy_binary function exists in binary_deploy module.

        Given: binary_deploy module is imported
        When: Checking for deploy_binary function
        Then: deploy_binary function should be defined
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer import binary_deploy

            assert hasattr(binary_deploy, "deploy_binary"), (
                "deploy_binary function not found in binary_deploy module\n"
                "Expected: def deploy_binary(source_dir, target_dir, platform)"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_binary_creates_target_directory(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify deploy_binary creates .treelint/bin/ directory.

        Given: A target project directory without .treelint/bin/
        When: deploy_binary is called
        Then: .treelint/bin/ directory should be created
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            # Deploy for Linux x86_64
            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="linux-x86_64",
            )

            expected_dir = temp_target_dir / ".treelint" / "bin"
            assert expected_dir.exists(), (
                f".treelint/bin/ directory not created: {expected_dir}\n"
                "Expected: deploy_binary to create target directory"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_binary_copies_correct_platform_binary(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify deploy_binary copies correct platform binary.

        Given: Source binaries for multiple platforms
        When: deploy_binary is called for linux-x86_64
        Then: Only treelint-linux-x86_64 should be copied
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="linux-x86_64",
            )

            # Check that binary was deployed
            deployed_binary = temp_target_dir / ".treelint" / "bin" / "treelint"
            assert deployed_binary.exists(), (
                f"Deployed binary not found: {deployed_binary}\n"
                "Expected: treelint binary in .treelint/bin/"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_binary_windows_has_exe_extension(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify Windows deployment uses .exe extension.

        Given: Deploying on Windows platform
        When: deploy_binary is called for windows-x86_64
        Then: Deployed binary should be named treelint.exe
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="windows-x86_64",
            )

            deployed_binary = temp_target_dir / ".treelint" / "bin" / "treelint.exe"
            assert deployed_binary.exists(), (
                f"Windows binary with .exe not found: {deployed_binary}\n"
                "Expected: treelint.exe in .treelint/bin/ for Windows"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_binary_unix_no_exe_extension(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify Unix deployment does not use .exe extension.

        Given: Deploying on Linux platform
        When: deploy_binary is called for linux-x86_64
        Then: Deployed binary should be named treelint (no .exe)
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="linux-x86_64",
            )

            # Should be 'treelint', not 'treelint.exe'
            deployed_binary = temp_target_dir / ".treelint" / "bin" / "treelint"
            deployed_exe = temp_target_dir / ".treelint" / "bin" / "treelint.exe"

            assert deployed_binary.exists(), (
                f"Unix binary not found: {deployed_binary}"
            )
            assert not deployed_exe.exists(), (
                f"Unix binary should not have .exe extension: {deployed_exe}"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    @pytest.mark.parametrize(
        "platform",
        [
            "linux-x86_64",
            "linux-aarch64",
            "darwin-x86_64",
            "darwin-aarch64",
            "windows-x86_64",
        ],
    )
    def test_deploy_binary_supports_all_platforms(
        self, project_root: Path, temp_source_dir: Path, tmp_path: Path, platform: str
    ):
        """
        Test: Verify deploy_binary supports all 5 platforms.

        Given: Source binaries for all platforms
        When: deploy_binary is called for each platform
        Then: Deployment should succeed for all platforms
        """
        # Create fresh target for each parametrized run
        temp_target_dir = tmp_path / f"target_{platform.replace('-', '_')}"
        temp_target_dir.mkdir(parents=True, exist_ok=True)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            # Should not raise exception
            deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform=platform,
            )

            # Verify deployment succeeded
            bin_dir = temp_target_dir / ".treelint" / "bin"
            assert bin_dir.exists(), f"Failed to deploy for platform: {platform}"

            # Check binary exists (with or without .exe)
            binary_name = "treelint.exe" if "windows" in platform else "treelint"
            binary_path = bin_dir / binary_name
            assert binary_path.exists(), (
                f"Binary not deployed for {platform}: {binary_path}"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_binary_returns_deployment_result(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify deploy_binary returns deployment result info.

        Given: Successful binary deployment
        When: deploy_binary is called
        Then: Should return result with status, path, and platform info
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            result = deploy_binary(
                source_dir=temp_source_dir,
                target_dir=temp_target_dir,
                platform="linux-x86_64",
            )

            assert result is not None, "deploy_binary should return result"
            assert hasattr(result, "success") or isinstance(result, dict), (
                "Result should have success attribute or be a dict"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_binary_raises_on_missing_source(
        self, project_root: Path, temp_target_dir: Path, tmp_path: Path
    ):
        """
        Test: Verify deploy_binary raises error for missing source binary.

        Given: Source directory without the requested platform binary
        When: deploy_binary is called
        Then: Should raise appropriate exception
        """
        empty_source = tmp_path / "empty_source"
        empty_source.mkdir(parents=True, exist_ok=True)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            with pytest.raises((FileNotFoundError, ValueError)):
                deploy_binary(
                    source_dir=empty_source,
                    target_dir=temp_target_dir,
                    platform="linux-x86_64",
                )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_binary_raises_on_invalid_platform(
        self, project_root: Path, temp_source_dir: Path, temp_target_dir: Path
    ):
        """
        Test: Verify deploy_binary raises error for invalid platform.

        Given: Valid source directory
        When: deploy_binary is called with unsupported platform
        Then: Should raise ValueError
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            with pytest.raises(ValueError):
                deploy_binary(
                    source_dir=temp_source_dir,
                    target_dir=temp_target_dir,
                    platform="invalid-platform",
                )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)
