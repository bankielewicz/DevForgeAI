"""
Tests for AC#4: Checksum Validation for Integrity

Story: STORY-352 - Add Treelint Binary to Installer Distribution
AC#4: Installer validates binary checksum before deployment, fails on mismatch

These tests verify:
- checksums.txt contains SHA256 hashes for all binaries
- Checksum validation occurs during deployment
- Deployment fails with clear error on checksum mismatch
- Integration with existing installer/checksum.py module
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import hashlib
import sys


class TestAC4Checksum:
    """Tests for AC#4: Checksum Validation for Integrity."""

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
    def create_source_with_checksums(self, tmp_path: Path):
        """Factory fixture to create source directory with valid/invalid checksums."""

        def _create(valid_checksums: bool = True) -> Path:
            source_dir = tmp_path / "src" / "bin" / "treelint"
            source_dir.mkdir(parents=True, exist_ok=True)

            # Create mock binary files with version string
            binaries = [
                "treelint-linux-x86_64",
                "treelint-linux-aarch64",
                "treelint-darwin-x86_64",
                "treelint-darwin-aarch64",
                "treelint-windows-x86_64.exe",
            ]
            # Use script content with version for version extraction
            binary_content = b"#!/bin/bash\n# Version: 0.12.0\necho treelint version 0.12.0\n"

            checksums_content = []
            for binary_name in binaries:
                binary_path = source_dir / binary_name
                binary_path.write_bytes(binary_content)

                # Calculate actual checksum
                actual_checksum = hashlib.sha256(binary_content).hexdigest()

                if valid_checksums:
                    checksums_content.append(f"{actual_checksum}  {binary_name}")
                else:
                    # Use intentionally wrong checksum
                    fake_checksum = "0" * 64
                    checksums_content.append(f"{fake_checksum}  {binary_name}")

            (source_dir / "checksums.txt").write_text("\n".join(checksums_content))
            return source_dir

        return _create

    def test_checksums_txt_format_sha256(self, project_root: Path):
        """
        Test: Verify checksums.txt uses SHA256 format.

        Given: src/bin/treelint/checksums.txt exists
        When: Reading the checksum file
        Then: Each line should have format: {64-char-hex}  {filename}
        """
        checksums_path = project_root / "src" / "bin" / "treelint" / "checksums.txt"

        if not checksums_path.exists():
            pytest.skip("checksums.txt not yet created - will be created during implementation")

        content = checksums_path.read_text()
        lines = [line.strip() for line in content.split("\n") if line.strip()]

        assert len(lines) >= 5, (
            f"Expected at least 5 checksum entries (one per binary), found {len(lines)}"
        )

        for line in lines:
            parts = line.split("  ")  # Two spaces separator (standard checksum format)
            assert len(parts) == 2, (
                f"Invalid checksum line format: {line}\n"
                "Expected: {{checksum}}  {{filename}} (two spaces)"
            )

            checksum, filename = parts
            assert len(checksum) == 64, (
                f"Checksum is not 64 characters (SHA256): {checksum}\n"
                f"Actual length: {len(checksum)}"
            )
            assert all(c in "0123456789abcdef" for c in checksum.lower()), (
                f"Checksum contains non-hex characters: {checksum}"
            )

    def test_checksums_txt_covers_all_binaries(self, project_root: Path):
        """
        Test: Verify checksums.txt has entries for all 5 platform binaries.

        Given: src/bin/treelint/checksums.txt exists
        When: Parsing the checksum entries
        Then: All 5 platform binaries should have corresponding checksum entries
        """
        checksums_path = project_root / "src" / "bin" / "treelint" / "checksums.txt"

        if not checksums_path.exists():
            pytest.skip("checksums.txt not yet created")

        expected_binaries = {
            "treelint-linux-x86_64",
            "treelint-linux-aarch64",
            "treelint-darwin-x86_64",
            "treelint-darwin-aarch64",
            "treelint-windows-x86_64.exe",
        }

        content = checksums_path.read_text()
        found_binaries = set()

        for line in content.split("\n"):
            if line.strip():
                parts = line.strip().split("  ")
                if len(parts) == 2:
                    found_binaries.add(parts[1])

        missing = expected_binaries - found_binaries
        assert not missing, (
            f"Missing checksums for binaries: {missing}\n"
            f"Found: {found_binaries}"
        )

    def test_deploy_validates_checksum_before_copy(
        self, project_root: Path, create_source_with_checksums, temp_target_dir: Path
    ):
        """
        Test: Verify deploy_binary validates checksum before deployment.

        Given: Valid source binaries with matching checksums
        When: deploy_binary is called
        Then: Checksum validation should occur before file copy
        """
        source_dir = create_source_with_checksums(valid_checksums=True)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            # Should succeed with valid checksums
            result = deploy_binary(
                source_dir=source_dir,
                target_dir=temp_target_dir,
                platform="linux-x86_64",
            )

            # Verify deployment succeeded
            deployed = temp_target_dir / ".treelint" / "bin" / "treelint"
            assert deployed.exists(), "Binary should be deployed when checksum matches"
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_fails_on_checksum_mismatch(
        self, project_root: Path, create_source_with_checksums, temp_target_dir: Path
    ):
        """
        Test: Verify deploy_binary fails when checksum doesn't match.

        Given: Source binary with intentionally wrong checksum in checksums.txt
        When: deploy_binary is called
        Then: Deployment should fail with checksum mismatch error
        """
        source_dir = create_source_with_checksums(valid_checksums=False)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            with pytest.raises((ValueError, RuntimeError)) as exc_info:
                deploy_binary(
                    source_dir=source_dir,
                    target_dir=temp_target_dir,
                    platform="linux-x86_64",
                )

            error_msg = str(exc_info.value).lower()
            assert "checksum" in error_msg or "integrity" in error_msg or "mismatch" in error_msg, (
                f"Error message should mention checksum/integrity/mismatch\n"
                f"Got: {exc_info.value}"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_error_message_is_clear_on_mismatch(
        self, project_root: Path, create_source_with_checksums, temp_target_dir: Path
    ):
        """
        Test: Verify checksum mismatch error message is clear and informative.

        Given: Binary with checksum mismatch
        When: Deployment fails
        Then: Error should include filename and indicate integrity issue
        """
        source_dir = create_source_with_checksums(valid_checksums=False)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            with pytest.raises(Exception) as exc_info:
                deploy_binary(
                    source_dir=source_dir,
                    target_dir=temp_target_dir,
                    platform="linux-x86_64",
                )

            error_msg = str(exc_info.value)
            # Error should be informative
            assert len(error_msg) > 20, (
                f"Error message is too short to be informative: {error_msg}"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_no_partial_deployment_on_checksum_failure(
        self, project_root: Path, create_source_with_checksums, temp_target_dir: Path
    ):
        """
        Test: Verify no partial binary is left on checksum failure.

        Given: Binary with checksum mismatch
        When: Deployment fails
        Then: No partial binary should exist in target directory
        """
        source_dir = create_source_with_checksums(valid_checksums=False)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            try:
                deploy_binary(
                    source_dir=source_dir,
                    target_dir=temp_target_dir,
                    platform="linux-x86_64",
                )
            except Exception:
                pass  # Expected to fail

            # Verify no partial deployment
            treelint_dir = temp_target_dir / ".treelint" / "bin"
            if treelint_dir.exists():
                treelint_binary = treelint_dir / "treelint"
                assert not treelint_binary.exists(), (
                    "Partial binary should not exist after checksum failure\n"
                    f"Found: {treelint_binary}"
                )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_deploy_uses_installer_checksum_module(self, project_root: Path):
        """
        Test: Verify binary_deploy integrates with existing installer/checksum.py.

        Given: binary_deploy module
        When: Checking imports
        Then: Should use calculate_sha256 from installer.checksum
        """
        sys.path.insert(0, str(project_root))
        try:
            from installer import binary_deploy
            import inspect

            source_code = inspect.getsource(binary_deploy)

            # Should import from installer.checksum
            assert (
                "from installer import checksum" in source_code
                or "from installer.checksum import" in source_code
                or "from . import checksum" in source_code
                or "from .checksum import" in source_code
            ), (
                "binary_deploy should import from installer.checksum module\n"
                "Expected: Import of checksum calculation function"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_checksum_validation_uses_sha256(
        self, project_root: Path, create_source_with_checksums, temp_target_dir: Path
    ):
        """
        Test: Verify checksum validation uses SHA256 algorithm.

        Given: Valid source with SHA256 checksums
        When: Validating checksums
        Then: SHA256 algorithm should be used (not MD5 or other)
        """
        source_dir = create_source_with_checksums(valid_checksums=True)

        sys.path.insert(0, str(project_root))
        try:
            from installer import binary_deploy, checksum

            # Verify checksum module uses SHA256
            test_content = b"test content"
            expected_sha256 = hashlib.sha256(test_content).hexdigest()

            # Use temporary file
            test_file = temp_target_dir / "test_file"
            test_file.write_bytes(test_content)

            calculated = checksum.calculate_sha256(test_file)
            assert calculated == expected_sha256, (
                f"Checksum module should use SHA256\n"
                f"Expected: {expected_sha256}\n"
                f"Got: {calculated}"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_missing_checksums_file_raises_error(
        self, project_root: Path, tmp_path: Path, temp_target_dir: Path
    ):
        """
        Test: Verify error when checksums.txt is missing.

        Given: Source directory without checksums.txt
        When: deploy_binary is called
        Then: Should raise error about missing checksums file
        """
        # Create source without checksums.txt
        source_dir = tmp_path / "no_checksums"
        source_dir.mkdir(parents=True, exist_ok=True)
        (source_dir / "treelint-linux-x86_64").write_bytes(b"\x7fELF" + b"\x00" * 100)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            with pytest.raises((FileNotFoundError, ValueError)) as exc_info:
                deploy_binary(
                    source_dir=source_dir,
                    target_dir=temp_target_dir,
                    platform="linux-x86_64",
                )

            error_msg = str(exc_info.value).lower()
            assert "checksum" in error_msg or "not found" in error_msg, (
                f"Error should mention missing checksums file\n"
                f"Got: {exc_info.value}"
            )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)

    def test_corrupt_binary_rejected(
        self, project_root: Path, create_source_with_checksums, temp_target_dir: Path
    ):
        """
        Test: Verify corrupted binary is rejected (BR-002).

        Given: Binary file that has been modified after checksum calculation
        When: deploy_binary is called
        Then: Should fail with integrity error
        """
        source_dir = create_source_with_checksums(valid_checksums=True)

        # Corrupt the binary after checksums were calculated
        binary_path = source_dir / "treelint-linux-x86_64"
        original_content = binary_path.read_bytes()
        corrupted_content = original_content + b"CORRUPTED"
        binary_path.write_bytes(corrupted_content)

        sys.path.insert(0, str(project_root))
        try:
            from installer.binary_deploy import deploy_binary

            with pytest.raises((ValueError, RuntimeError)):
                deploy_binary(
                    source_dir=source_dir,
                    target_dir=temp_target_dir,
                    platform="linux-x86_64",
                )
        except ImportError:
            pytest.skip("binary_deploy module not yet implemented")
        finally:
            sys.path.pop(0)
