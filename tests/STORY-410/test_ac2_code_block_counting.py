"""
Test: AC#2 - Script Counts Code Blocks Before Skill Invocation
Story: STORY-410
Generated: 2026-02-16

Given: A command file contains Skill() invocations
When: The script analyzes the file
Then: It counts code blocks (```) appearing before the first Skill() call
"""
import pytest


class TestAC2CodeBlockCounting:
    """AC#2: Script counts triple-backtick code blocks before first Skill() line."""

    def test_ac2_counts_2_blocks_for_clean_command(self, run_audit, fixtures_dir):
        """clean-command.md has 1 code block (open+close = 2 backtick lines) before Skill()."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert - clean-command should show 2 code block markers (1 block = open + close)
        # The script counts ``` occurrences, so 1 code block = 2 triple-backtick lines
        assert "clean-command.md" in result.stdout
        # Expect count of 2 (one opening ```, one closing ```)
        assert "2 code block" in result.stdout or "(2" in result.stdout, (
            f"Expected 2 backtick lines for clean-command.md. Output: {result.stdout}"
        )

    def test_ac2_counts_12_blocks_for_violation_command(self, run_audit, fixtures_dir):
        """violation-command.md has 6 code blocks (12 backtick lines) before Skill()."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        assert "violation-command.md" in result.stdout
        assert "12" in result.stdout, (
            f"Expected 12 backtick lines for violation-command.md. Output: {result.stdout}"
        )

    def test_ac2_counts_8_blocks_for_boundary_command(self, run_audit, fixtures_dir):
        """boundary-command.md has 4 code blocks (8 backtick lines) before Skill()."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        assert "boundary-command.md" in result.stdout
        assert "8" in result.stdout or "(8" in result.stdout, (
            f"Expected 8 backtick lines for boundary-command.md. Output: {result.stdout}"
        )

    def test_ac2_stops_counting_at_first_skill_line(self, run_audit, tmp_path):
        """Code blocks AFTER Skill() should not be counted."""
        # Arrange
        cmd_dir = tmp_path / "cmds"
        cmd_dir.mkdir()
        (cmd_dir / "after-skill.md").write_text(
            "# Test\n"
            "```bash\necho hi\n```\n"
            "Skill(command=\"test\")\n"
            "```bash\necho after\n```\n"
            "```bash\necho after2\n```\n"
        )

        # Act
        result = run_audit(str(cmd_dir))

        # Assert - should count only 2 (one block before Skill)
        assert "2" in result.stdout, (
            f"Should count only blocks before Skill(). Output: {result.stdout}"
        )
