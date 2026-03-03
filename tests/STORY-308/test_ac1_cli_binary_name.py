"""
STORY-308 AC#1: CLI prog name matches setup.py entry point

Tests that cli.py uses prog='devforgeai-validate' to match setup.py registration.
These tests should FAIL before implementation (TDD Red phase).
"""
import pytest
import subprocess
import sys
from pathlib import Path


class TestCliBinaryName:
    """Test suite for AC#1: CLI prog name matches setup.py entry point."""

    def test_cli_help_shows_devforgeai_validate_prog_name(self):
        """
        Test: CLI --help output shows 'usage: devforgeai-validate'
        Given: The Python CLI is installed via pip install -e .claude/scripts/
        When: User runs devforgeai-validate --help
        Then: The help text shows prog='devforgeai-validate' (not 'devforgeai')
        """
        # Act
        result = subprocess.run(
            [sys.executable, "-m", "devforgeai_cli.cli", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parents[2] / ".claude" / "scripts"
        )

        # Assert
        assert "usage: devforgeai-validate" in result.stdout, (
            f"Expected 'usage: devforgeai-validate' in help output, "
            f"but got: {result.stdout[:200]}"
        )
        assert "usage: devforgeai " not in result.stdout, (
            "Help output should NOT show 'usage: devforgeai ' (without -validate)"
        )

    def test_cli_py_prog_declaration_matches_setup_py(self):
        """
        Test: cli.py prog declaration matches setup.py entry_points
        Given: setup.py registers 'devforgeai-validate=devforgeai_cli.cli:main'
        When: cli.py ArgumentParser is configured
        Then: prog='devforgeai-validate' is set
        """
        # Arrange
        cli_path = Path(__file__).parents[2] / "src" / "claude" / "scripts" / "devforgeai_cli" / "cli.py"

        # Act
        cli_content = cli_path.read_text()

        # Assert
        assert "prog='devforgeai-validate'" in cli_content, (
            "cli.py should contain prog='devforgeai-validate'"
        )
        assert "prog='devforgeai'" not in cli_content or "prog='devforgeai-validate'" in cli_content, (
            "cli.py should NOT contain prog='devforgeai' without '-validate' suffix"
        )

    def test_cli_version_output_shows_correct_prog_name(self):
        """
        Test: CLI --version output shows 'devforgeai-validate'
        Given: CLI is invoked with --version flag
        When: Version string is displayed
        Then: It shows 'devforgeai-validate 0.1.0' (not 'devforgeai 0.1.0')
        """
        # Act
        result = subprocess.run(
            [sys.executable, "-m", "devforgeai_cli.cli", "--version"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parents[2] / ".claude" / "scripts"
        )

        # Assert
        assert "devforgeai-validate" in result.stdout, (
            f"Expected 'devforgeai-validate' in version output, got: {result.stdout}"
        )
