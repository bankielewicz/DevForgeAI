"""
Test: AC#5 - File Size Constraints
Story: STORY-540
TDD Phase: Red (tests must FAIL before implementation)

Validates:
- Skill reference file (positioning-strategy.md) < 1,000 lines
- Associated command file < 500 lines (if exists)
"""
import os
import pytest

from conftest import PROJECT_ROOT


SKILL_REFERENCE_FILE = os.path.join(
    PROJECT_ROOT,
    "src", "claude", "skills", "marketing-business", "references",
    "positioning-strategy.md",
)

# Command file path (marketing-plan or similar)
COMMAND_FILE_CANDIDATES = [
    os.path.join(PROJECT_ROOT, "src", "claude", "commands", "marketing-plan.md"),
    os.path.join(PROJECT_ROOT, "src", "claude", "commands", "positioning.md"),
]


class TestSkillReferenceFileLineLimit:
    """Verify skill reference file is strictly under 1,000 lines."""

    def test_should_exist_as_file(self):
        assert os.path.isfile(SKILL_REFERENCE_FILE), (
            f"Skill reference file does not exist: {SKILL_REFERENCE_FILE}"
        )

    def test_should_be_under_1000_lines(self):
        assert os.path.isfile(SKILL_REFERENCE_FILE), (
            f"Cannot check line count - file does not exist: {SKILL_REFERENCE_FILE}"
        )
        with open(SKILL_REFERENCE_FILE, "r", encoding="utf-8") as fh:
            line_count = sum(1 for _ in fh)
        assert line_count < 1000, (
            f"Skill reference file is {line_count} lines, must be < 1,000"
        )


class TestCommandFileLineLimit:
    """Verify any associated command file is strictly under 500 lines."""

    def _find_command_file(self):
        """Return the first existing command file candidate, or None."""
        for path in COMMAND_FILE_CANDIDATES:
            if os.path.isfile(path):
                return path
        return None

    def test_should_have_command_file_under_500_lines_if_exists(self):
        cmd_file = self._find_command_file()
        if cmd_file is None:
            pytest.skip("No command file found yet (will be created during implementation)")
        with open(cmd_file, "r", encoding="utf-8") as fh:
            line_count = sum(1 for _ in fh)
        assert line_count < 500, (
            f"Command file {cmd_file} is {line_count} lines, must be < 500"
        )
