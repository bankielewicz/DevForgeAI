"""
Test: AC#4 - Script Reports Clean Commands
Story: STORY-410
Generated: 2026-02-16

Given: A command file has <=4 code blocks before Skill() invocation
When: The script completes analysis
Then: The file is marked as clean with check-mark marker and code block count
"""
import pytest


class TestAC4CleanReporting:
    """AC#4: Clean commands get check-mark marker with block count."""

    def test_ac4_clean_command_gets_check_marker(self, run_audit, fixtures_dir):
        """clean-command.md has 1 code block (<=4), should show check-mark."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        lines = [l for l in result.stdout.splitlines() if "clean-command.md" in l]
        assert len(lines) > 0, "clean-command.md not in output"
        assert "\u2705" in lines[0], (
            f"Expected check-mark for clean command. Got: {lines[0]}"
        )

    def test_ac4_clean_output_shows_code_block_count(self, run_audit, fixtures_dir):
        """Clean command output should include the code block count."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        lines = [l for l in result.stdout.splitlines() if "clean-command.md" in l]
        assert len(lines) > 0
        # Should contain a number indicating block count
        assert any(char.isdigit() for char in lines[0]), (
            f"Expected code block count in output. Got: {lines[0]}"
        )

    def test_ac4_boundary_command_is_clean(self, run_audit, fixtures_dir):
        """boundary-command.md (exactly 4 blocks) should be marked clean."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        lines = [l for l in result.stdout.splitlines() if "boundary-command.md" in l]
        assert len(lines) > 0, "boundary-command.md not in output"
        assert "\u2705" in lines[0], (
            f"Boundary (4 blocks) should be clean. Got: {lines[0]}"
        )

    def test_ac4_zero_blocks_is_clean(self, run_audit, tmp_path):
        """A command with Skill() but zero code blocks should be clean."""
        # Arrange
        cmd_dir = tmp_path / "cmds"
        cmd_dir.mkdir()
        (cmd_dir / "zero-blocks.md").write_text(
            "# Zero blocks\nSome text\nSkill(command=\"test\")\n"
        )

        # Act
        result = run_audit(str(cmd_dir))

        # Assert
        assert "\u2705" in result.stdout, (
            f"Zero blocks should be clean. Output: {result.stdout}"
        )
