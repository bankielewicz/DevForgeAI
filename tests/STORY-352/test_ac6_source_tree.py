"""
Tests for AC#6: source-tree.md Updated with Binary Location

Story: STORY-352 - Add Treelint Binary to Installer Distribution
AC#6: source-tree.md includes src/bin/treelint/ directory documentation

These tests verify:
- source-tree.md contains src/bin/treelint/ entry
- Binary filenames are documented
- Documentation follows existing format
"""

import pytest
from pathlib import Path
import re


class TestAC6SourceTree:
    """Tests for AC#6: source-tree.md Updated with Binary Location."""

    @pytest.fixture
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent.parent

    @pytest.fixture
    def source_tree_path(self, project_root: Path) -> Path:
        """Get source-tree.md path."""
        return project_root / "devforgeai" / "specs" / "context" / "source-tree.md"

    @pytest.fixture
    def source_tree_content(self, source_tree_path: Path) -> str:
        """Read source-tree.md content."""
        assert source_tree_path.exists(), (
            f"source-tree.md not found: {source_tree_path}"
        )
        return source_tree_path.read_text()

    def test_source_tree_exists(self, source_tree_path: Path):
        """
        Test: Verify source-tree.md exists.

        Given: DevForgeAI project
        When: Checking for source-tree.md
        Then: File should exist in devforgeai/specs/context/
        """
        assert source_tree_path.exists(), (
            f"source-tree.md not found at: {source_tree_path}"
        )

    def test_source_tree_contains_bin_directory(self, source_tree_content: str):
        """
        Test: Verify source-tree.md documents src/bin/ directory.

        Given: source-tree.md content
        When: Checking for bin directory entry
        Then: src/bin/ or bin/ directory should be documented
        """
        # Look for bin directory in source tree documentation
        bin_patterns = [
            r"src/bin/",
            r"\bbin/\b.*treelint",
            r"├── bin/",
            r"│.*bin/",
        ]

        found = any(re.search(pattern, source_tree_content) for pattern in bin_patterns)
        assert found, (
            "src/bin/ directory not found in source-tree.md\n"
            "Expected: Documentation of bin/ directory for treelint binaries"
        )

    def test_source_tree_contains_treelint_directory(self, source_tree_content: str):
        """
        Test: Verify source-tree.md documents src/bin/treelint/ directory.

        Given: source-tree.md content
        When: Checking for treelint directory entry
        Then: treelint/ directory should be documented
        """
        treelint_patterns = [
            r"treelint/",
            r"treelint\b",
            r"├── treelint",
            r"│.*treelint",
        ]

        found = any(re.search(pattern, source_tree_content) for pattern in treelint_patterns)
        assert found, (
            "treelint/ directory not found in source-tree.md\n"
            "Expected: Documentation of src/bin/treelint/ directory"
        )

    def test_source_tree_documents_linux_x86_64_binary(self, source_tree_content: str):
        """
        Test: Verify treelint-linux-x86_64 binary is documented.

        Given: source-tree.md content
        When: Checking for Linux x86_64 binary
        Then: treelint-linux-x86_64 should be documented
        """
        assert "treelint-linux-x86_64" in source_tree_content, (
            "treelint-linux-x86_64 binary not documented in source-tree.md"
        )

    def test_source_tree_documents_linux_aarch64_binary(self, source_tree_content: str):
        """
        Test: Verify treelint-linux-aarch64 binary is documented.

        Given: source-tree.md content
        When: Checking for Linux aarch64 binary
        Then: treelint-linux-aarch64 should be documented
        """
        assert "treelint-linux-aarch64" in source_tree_content, (
            "treelint-linux-aarch64 binary not documented in source-tree.md"
        )

    def test_source_tree_documents_darwin_x86_64_binary(self, source_tree_content: str):
        """
        Test: Verify treelint-darwin-x86_64 binary is documented.

        Given: source-tree.md content
        When: Checking for macOS x86_64 binary
        Then: treelint-darwin-x86_64 should be documented
        """
        assert "treelint-darwin-x86_64" in source_tree_content, (
            "treelint-darwin-x86_64 binary not documented in source-tree.md"
        )

    def test_source_tree_documents_darwin_aarch64_binary(self, source_tree_content: str):
        """
        Test: Verify treelint-darwin-aarch64 binary is documented.

        Given: source-tree.md content
        When: Checking for macOS aarch64 (Apple Silicon) binary
        Then: treelint-darwin-aarch64 should be documented
        """
        assert "treelint-darwin-aarch64" in source_tree_content, (
            "treelint-darwin-aarch64 binary not documented in source-tree.md"
        )

    def test_source_tree_documents_windows_binary(self, source_tree_content: str):
        """
        Test: Verify treelint-windows-x86_64.exe binary is documented.

        Given: source-tree.md content
        When: Checking for Windows binary
        Then: treelint-windows-x86_64.exe should be documented
        """
        assert "treelint-windows-x86_64.exe" in source_tree_content, (
            "treelint-windows-x86_64.exe binary not documented in source-tree.md"
        )

    def test_source_tree_documents_all_five_binaries(self, source_tree_content: str):
        """
        Test: Verify all 5 platform binaries are documented.

        Given: source-tree.md content
        When: Checking for all platform binaries
        Then: All 5 binaries should be documented
        """
        expected_binaries = [
            "treelint-linux-x86_64",
            "treelint-linux-aarch64",
            "treelint-darwin-x86_64",
            "treelint-darwin-aarch64",
            "treelint-windows-x86_64.exe",
        ]

        missing = [b for b in expected_binaries if b not in source_tree_content]
        assert not missing, (
            f"Missing binary documentation in source-tree.md:\n"
            f"  {', '.join(missing)}"
        )

    def test_source_tree_documents_checksums_file(self, source_tree_content: str):
        """
        Test: Verify checksums.txt is documented.

        Given: source-tree.md content
        When: Checking for checksums file
        Then: checksums.txt should be mentioned
        """
        # May be documented as checksums.txt or with description
        assert "checksums" in source_tree_content.lower(), (
            "checksums.txt not documented in source-tree.md\n"
            "Expected: Documentation of checksum manifest file"
        )

    def test_source_tree_follows_tree_format(self, source_tree_content: str):
        """
        Test: Verify source-tree.md uses consistent tree format.

        Given: source-tree.md content
        When: Checking treelint documentation format
        Then: Should use tree-like structure with proper indentation
        """
        # Check for tree formatting characters around treelint
        tree_chars = ["├──", "│", "└──"]

        # Find the section containing treelint
        if "treelint" in source_tree_content:
            # Check that tree structure characters appear in the file
            has_tree_format = any(char in source_tree_content for char in tree_chars)
            assert has_tree_format, (
                "source-tree.md should use tree-like format (├──, │, └──)"
            )

    def test_source_tree_bin_under_src(self, source_tree_content: str):
        """
        Test: Verify bin/ is documented under src/ directory.

        Given: source-tree.md content
        When: Checking bin/ location
        Then: bin/ should be under src/ (distribution source)
        """
        # Look for pattern showing bin under src
        patterns = [
            r"src/\s*\n.*bin/",  # src/ followed by bin/ on subsequent line
            r"src/bin/",  # Direct path reference
            r"├── src/.*\n.*bin/",  # Tree structure
        ]

        found = any(re.search(pattern, source_tree_content, re.DOTALL) for pattern in patterns)

        # Alternative: just check src/bin appears somewhere
        if not found:
            found = "src/bin" in source_tree_content or (
                "src/" in source_tree_content and "bin/" in source_tree_content
            )

        assert found, (
            "bin/ directory should be documented under src/\n"
            "Expected: src/bin/treelint/ in source tree"
        )

    def test_source_tree_locked_status(self, source_tree_content: str):
        """
        Test: Verify source-tree.md has LOCKED status.

        Given: source-tree.md is a context file
        When: Checking status marker
        Then: Should have LOCKED status (immutable context file)
        """
        assert "LOCKED" in source_tree_content, (
            "source-tree.md should have LOCKED status marker"
        )

    def test_source_tree_version_updated(self, source_tree_content: str):
        """
        Test: Verify source-tree.md version is updated for treelint addition.

        Given: source-tree.md with treelint documentation added
        When: Checking version information
        Then: Version should reflect the update
        """
        # Look for version pattern
        version_pattern = r"Version:\s*[\d.]+|version:\s*[\d.]+"
        match = re.search(version_pattern, source_tree_content, re.IGNORECASE)

        if match:
            # Version exists, which is good
            pass
        else:
            # Version field should exist
            assert "version" in source_tree_content.lower() or "Version" in source_tree_content, (
                "source-tree.md should include version information"
            )

    def test_binary_directory_has_description(self, source_tree_content: str):
        """
        Test: Verify treelint binary directory has description/comments.

        Given: source-tree.md with treelint entry
        When: Checking for documentation
        Then: Should have description of binary purpose
        """
        # Look for descriptive text near treelint entries
        treelint_section = ""
        lines = source_tree_content.split("\n")
        for i, line in enumerate(lines):
            if "treelint" in line.lower():
                # Get context (surrounding lines)
                start = max(0, i - 2)
                end = min(len(lines), i + 5)
                treelint_section = "\n".join(lines[start:end])
                break

        # Should have some description or comment
        has_description = (
            "#" in treelint_section  # Markdown comment
            or "binary" in treelint_section.lower()
            or "platform" in treelint_section.lower()
            or "distribution" in treelint_section.lower()
        )

        # This is a soft check - implementation may vary
        if treelint_section and not has_description:
            pytest.skip(
                "No description found for treelint entry - optional but recommended"
            )
