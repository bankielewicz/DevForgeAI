"""
Test: AC#3 - Script Flags Violations Based on Threshold
Story: STORY-410
Generated: 2026-02-16

Given: A command file has >4 code blocks before Skill() invocation
When: The script completes analysis
Then: The file is flagged as a potential hybrid violation with cross-mark marker
"""
import pytest


class TestAC3ViolationFlagging:
    """AC#3: Files with >4 code blocks before Skill() get flagged."""

    def test_ac3_violation_command_gets_cross_marker(self, run_audit, fixtures_dir):
        """violation-command.md has 12 backtick lines (>4), should show cross-mark."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        # Find the line containing violation-command.md
        lines = result.stdout.splitlines()
        violation_lines = [l for l in lines if "violation-command.md" in l]
        assert len(violation_lines) > 0, "violation-command.md not in output"
        assert "\u274c" in violation_lines[0], (
            f"Expected cross-mark marker for violation. Got: {violation_lines[0]}"
        )

    def test_ac3_violation_output_mentions_hybrid(self, run_audit, fixtures_dir):
        """Violation output should mention 'hybrid violation' or similar."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert
        lines = [l for l in result.stdout.splitlines() if "violation-command.md" in l]
        assert any("hybrid" in l.lower() or "violation" in l.lower() for l in lines), (
            f"Expected 'hybrid violation' text. Got: {lines}"
        )

    def test_ac3_threshold_boundary_4_is_clean(self, run_audit, fixtures_dir):
        """boundary-command.md has exactly 4 code blocks (8 backtick lines).
        Per BR-001: count > 4 triggers violation. 4 should NOT trigger."""
        # Act
        result = run_audit(fixtures_dir)

        # Assert - boundary should NOT have cross-mark
        lines = [l for l in result.stdout.splitlines() if "boundary-command.md" in l]
        assert len(lines) > 0, "boundary-command.md not in output"
        assert "\u274c" not in lines[0], (
            f"Boundary (4 blocks) should NOT be flagged. Got: {lines[0]}"
        )

    def test_ac3_threshold_boundary_5_is_violation(self, run_audit, tmp_path):
        """A file with exactly 5 code blocks should be flagged."""
        # Arrange
        cmd_dir = tmp_path / "cmds"
        cmd_dir.mkdir()
        blocks = "".join(f"```bash\necho {i}\n```\n" for i in range(5))
        (cmd_dir / "five-blocks.md").write_text(
            f"# Five blocks\n{blocks}Skill(command=\"test\")\n"
        )

        # Act
        result = run_audit(str(cmd_dir))

        # Assert
        assert "\u274c" in result.stdout, (
            f"5 code blocks should trigger violation. Output: {result.stdout}"
        )
