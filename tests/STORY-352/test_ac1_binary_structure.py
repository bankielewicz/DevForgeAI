"""
Tests for AC#1: Treelint Binary Added to src/ Distribution Structure

Story: STORY-352 - Add Treelint Binary to Installer Distribution
AC#1: Platform-specific binaries exist at src/bin/treelint/ with correct naming convention

These tests verify:
- src/bin/treelint/ directory exists
- All 5 platform binaries are present with correct naming convention
- checksums.txt file exists in the binary directory
"""

import pytest
from pathlib import Path


class TestAC1BinaryStructure:
    """Tests for AC#1: Treelint Binary Added to src/ Distribution Structure."""

    @pytest.fixture
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent.parent

    @pytest.fixture
    def treelint_bin_dir(self, project_root: Path) -> Path:
        """Get treelint binary directory path."""
        return project_root / "src" / "bin" / "treelint"

    @pytest.fixture
    def expected_binaries(self) -> list[str]:
        """List of expected platform binaries."""
        return [
            "treelint-linux-x86_64",
            "treelint-linux-aarch64",
            "treelint-darwin-x86_64",
            "treelint-darwin-aarch64",
            "treelint-windows-x86_64.exe",
        ]

    def test_treelint_bin_directory_exists(self, treelint_bin_dir: Path):
        """
        Test: Verify src/bin/treelint/ directory exists.

        Given: The src/ directory contains framework distribution files
        When: Treelint binaries are added for distribution
        Then: The src/bin/treelint/ directory must exist
        """
        assert treelint_bin_dir.exists(), (
            f"Directory does not exist: {treelint_bin_dir}\n"
            "Expected: src/bin/treelint/ directory to be created"
        )
        assert treelint_bin_dir.is_dir(), (
            f"Path exists but is not a directory: {treelint_bin_dir}"
        )

    def test_linux_x86_64_binary_exists(self, treelint_bin_dir: Path):
        """
        Test: Verify treelint-linux-x86_64 binary exists.

        Given: The src/bin/treelint/ directory exists
        When: Checking for platform binaries
        Then: treelint-linux-x86_64 binary must be present
        """
        binary_path = treelint_bin_dir / "treelint-linux-x86_64"
        assert binary_path.exists(), (
            f"Linux x86_64 binary not found: {binary_path}\n"
            "Expected: treelint-linux-x86_64 binary in src/bin/treelint/"
        )

    def test_linux_aarch64_binary_exists(self, treelint_bin_dir: Path):
        """
        Test: Verify treelint-linux-aarch64 binary exists.

        Given: The src/bin/treelint/ directory exists
        When: Checking for platform binaries
        Then: treelint-linux-aarch64 binary must be present
        """
        binary_path = treelint_bin_dir / "treelint-linux-aarch64"
        assert binary_path.exists(), (
            f"Linux aarch64 binary not found: {binary_path}\n"
            "Expected: treelint-linux-aarch64 binary in src/bin/treelint/"
        )

    def test_darwin_x86_64_binary_exists(self, treelint_bin_dir: Path):
        """
        Test: Verify treelint-darwin-x86_64 binary exists.

        Given: The src/bin/treelint/ directory exists
        When: Checking for platform binaries
        Then: treelint-darwin-x86_64 binary must be present
        """
        binary_path = treelint_bin_dir / "treelint-darwin-x86_64"
        assert binary_path.exists(), (
            f"macOS x86_64 binary not found: {binary_path}\n"
            "Expected: treelint-darwin-x86_64 binary in src/bin/treelint/"
        )

    def test_darwin_aarch64_binary_exists(self, treelint_bin_dir: Path):
        """
        Test: Verify treelint-darwin-aarch64 binary exists.

        Given: The src/bin/treelint/ directory exists
        When: Checking for platform binaries
        Then: treelint-darwin-aarch64 (Apple Silicon) binary must be present
        """
        binary_path = treelint_bin_dir / "treelint-darwin-aarch64"
        assert binary_path.exists(), (
            f"macOS aarch64 binary not found: {binary_path}\n"
            "Expected: treelint-darwin-aarch64 binary in src/bin/treelint/"
        )

    def test_windows_x86_64_binary_exists(self, treelint_bin_dir: Path):
        """
        Test: Verify treelint-windows-x86_64.exe binary exists.

        Given: The src/bin/treelint/ directory exists
        When: Checking for platform binaries
        Then: treelint-windows-x86_64.exe binary must be present
        """
        binary_path = treelint_bin_dir / "treelint-windows-x86_64.exe"
        assert binary_path.exists(), (
            f"Windows x86_64 binary not found: {binary_path}\n"
            "Expected: treelint-windows-x86_64.exe binary in src/bin/treelint/"
        )

    def test_all_platform_binaries_present(
        self, treelint_bin_dir: Path, expected_binaries: list[str]
    ):
        """
        Test: Verify all 5 platform binaries are present.

        Given: The src/bin/treelint/ directory exists
        When: Checking for all platform binaries
        Then: All 5 binaries must be present (linux x86_64, linux aarch64,
              darwin x86_64, darwin aarch64, windows x86_64)
        """
        missing_binaries = []
        for binary_name in expected_binaries:
            binary_path = treelint_bin_dir / binary_name
            if not binary_path.exists():
                missing_binaries.append(binary_name)

        assert not missing_binaries, (
            f"Missing binaries in {treelint_bin_dir}:\n"
            f"  {', '.join(missing_binaries)}\n"
            f"Expected all 5 platform binaries to be present"
        )

    def test_checksums_file_exists(self, treelint_bin_dir: Path):
        """
        Test: Verify checksums.txt file exists in binary directory.

        Given: The src/bin/treelint/ directory with binaries
        When: Checking for checksum manifest
        Then: checksums.txt file must be present
        """
        checksums_path = treelint_bin_dir / "checksums.txt"
        assert checksums_path.exists(), (
            f"Checksums file not found: {checksums_path}\n"
            "Expected: checksums.txt in src/bin/treelint/"
        )

    def test_binary_naming_convention(
        self, treelint_bin_dir: Path, expected_binaries: list[str]
    ):
        """
        Test: Verify binary naming follows convention treelint-{platform}-{arch}[.exe].

        Given: Binaries in src/bin/treelint/
        When: Checking naming convention
        Then: All binaries should follow pattern treelint-{platform}-{arch}
              with .exe extension for Windows only
        """
        import re

        pattern = r"^treelint-(linux|darwin|windows)-(x86_64|aarch64)(\.exe)?$"

        for binary_name in expected_binaries:
            assert re.match(pattern, binary_name), (
                f"Binary name does not match convention: {binary_name}\n"
                f"Expected pattern: treelint-{{platform}}-{{arch}}[.exe]"
            )

            # Windows should have .exe, others should not
            if "windows" in binary_name:
                assert binary_name.endswith(".exe"), (
                    f"Windows binary missing .exe extension: {binary_name}"
                )
            else:
                assert not binary_name.endswith(".exe"), (
                    f"Non-Windows binary should not have .exe: {binary_name}"
                )

    def test_binaries_are_files_not_directories(
        self, treelint_bin_dir: Path, expected_binaries: list[str]
    ):
        """
        Test: Verify binaries are files, not directories.

        Given: Binaries in src/bin/treelint/
        When: Checking file types
        Then: All binary paths should be regular files
        """
        for binary_name in expected_binaries:
            binary_path = treelint_bin_dir / binary_name
            if binary_path.exists():
                assert binary_path.is_file(), (
                    f"Binary path is not a file: {binary_path}\n"
                    "Expected: Regular file, not directory or symlink"
                )

    def test_binaries_are_non_empty(
        self, treelint_bin_dir: Path, expected_binaries: list[str]
    ):
        """
        Test: Verify binaries have non-zero file size.

        Given: Binaries in src/bin/treelint/
        When: Checking file sizes
        Then: All binaries should have size > 0 bytes
        """
        for binary_name in expected_binaries:
            binary_path = treelint_bin_dir / binary_name
            if binary_path.exists():
                file_size = binary_path.stat().st_size
                assert file_size > 0, (
                    f"Binary file is empty: {binary_path}\n"
                    "Expected: Non-empty binary file"
                )
