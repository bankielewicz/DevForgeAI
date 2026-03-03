"""
Test: AC#1 - Script Locates All Command Files
Story: STORY-410
Generated: 2026-02-16

Given: The audit script is executed from project root
When: It scans the .claude/commands/ directory
Then: All .md files are identified for analysis
"""
import os
import subprocess
import pytest


class TestAC1LocateCommands:
    """AC#1: Script locates all command files in the commands directory."""

    def test_ac1_script_exists_at_expected_path(self, script_path):
        """Arrange: Script should exist at .claude/scripts/audit-command-skill-overlap.sh"""
        # Assert
        assert os.path.isfile(script_path), (
            f"Script not found at {script_path}. "
            "Implementation needed: create .claude/scripts/audit-command-skill-overlap.sh"
        )

    def test_ac1_script_is_executable(self, script_path):
        """Script should be executable."""
        assert os.access(script_path, os.X_OK), (
            f"Script at {script_path} is not executable"
        )

    def test_ac1_finds_all_md_files_in_directory(self, run_audit, fixtures_dir):
        """Given fixture commands, script output should reference each .md file."""
        # Arrange - fixtures_dir has 5 .md files
        expected_files = [
            "clean-command.md",
            "violation-command.md",
            "no-skill-command.md",
            "boundary-command.md",
            "empty-command.md",
        ]

        # Act
        result = run_audit(fixtures_dir)

        # Assert - each file should appear in output
        for filename in expected_files:
            assert filename in result.stdout, (
                f"Script output missing reference to {filename}. "
                f"Output was: {result.stdout}"
            )

    def test_ac1_handles_empty_directory(self, run_audit, tmp_path):
        """Script should handle a directory with no .md files gracefully."""
        # Arrange
        empty_dir = tmp_path / "empty_commands"
        empty_dir.mkdir()

        # Act
        result = run_audit(str(empty_dir))

        # Assert - should not crash (exit code 0 or informational)
        assert result.returncode == 0, (
            f"Script crashed on empty directory. stderr: {result.stderr}"
        )

    def test_ac1_exit_code_1_when_violations_present(self, run_audit, fixtures_dir):
        """Script should exit 1 when violations detected (violation-command.md has >4 blocks)."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert - fixtures include violation-command.md with 6 code blocks (12 backtick lines)
        assert result.returncode == 1, (
            f"Expected exit code 1 when violations present. Got: {result.returncode}"
        )

    def test_ac1_nonexistent_directory_returns_error(self, run_audit):
        """Script should exit 1 with error when COMMANDS_DIR doesn't exist."""
        # Act
        result = run_audit("/nonexistent/path/to/commands")

        # Assert
        assert result.returncode == 1, (
            f"Expected exit code 1 for nonexistent directory. Got: {result.returncode}"
        )
        assert "Directory not found" in result.stderr, (
            f"Expected 'Directory not found' in stderr. Got: {result.stderr}"
        )
