"""
Test: AC#5 - Script Handles Commands Without Skill Invocations
Story: STORY-410
Generated: 2026-02-16

Given: A command file contains no Skill() invocations
When: The script analyzes the file
Then: It reports a warning with warning-sign "No Skill() invocation found"
"""
import pytest


class TestAC5NoSkillWarning:
    """AC#5: Commands without Skill() get warning marker."""

    def test_ac5_no_skill_command_gets_warning_marker(self, run_audit, fixtures_dir):
        """no-skill-command.md has no Skill() call, should show warning sign."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        lines = [l for l in result.stdout.splitlines() if "no-skill-command.md" in l]
        assert len(lines) > 0, "no-skill-command.md not in output"
        assert "\u26a0\ufe0f" in lines[0] or "\u26a0" in lines[0], (
            f"Expected warning marker for no-skill command. Got: {lines[0]}"
        )

    def test_ac5_no_skill_message_text(self, run_audit, fixtures_dir):
        """Warning should mention 'No Skill() invocation found'."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        lines = [l for l in result.stdout.splitlines() if "no-skill-command.md" in l]
        assert any("no skill" in l.lower() or "invocation" in l.lower() for l in lines), (
            f"Expected 'No Skill() invocation' message. Got: {lines}"
        )

    def test_ac5_no_skill_is_warning_not_error(self, run_audit, fixtures_dir):
        """Per BR-002: no-skill commands get warning, not cross-mark error."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        lines = [l for l in result.stdout.splitlines() if "no-skill-command.md" in l]
        assert len(lines) > 0
        assert "\u274c" not in lines[0], (
            f"No-skill should be warning, not error. Got: {lines[0]}"
        )

    def test_ac5_empty_file_handled_gracefully(self, run_audit, fixtures_dir):
        """empty-command.md should not crash the script."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert - script should complete without crash
        assert result.returncode == 0 or "empty-command.md" in result.stdout, (
            f"Script may have crashed on empty file. "
            f"rc={result.returncode}, stderr={result.stderr}"
        )
