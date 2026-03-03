"""AC#7: Cross-Reference Sweep Complete."""
import os
import subprocess

from conftest import PROJECT_ROOT

EXCLUDED_DIRS = [
    "devforgeai/feedback",
    "devforgeai/RCA",
    "devforgeai/specs/Stories",
    "devforgeai/specs/enhancements",
    ".claude/skills/devforgeai-development.backup",
    "src/claude/skills/devforgeai-development.backup",
    "tests/STORY-441",
]


class TestAC7CrossReferenceSweep:
    """AC#7: No active code references devforgeai-ideation."""

    def test_should_have_zero_matches_in_active_src_code(self):
        result = subprocess.run(
            ["grep", "-r", "--include=*.md", "--include=*.py", "--include=*.yaml",
             "--include=*.yml", "--include=*.json", "--include=*.ts",
             "devforgeai-ideation", os.path.join(PROJECT_ROOT, "src")],
            capture_output=True, text=True
        )
        matches = [
            line for line in result.stdout.strip().split("\n")
            if line and not any(excl in line for excl in EXCLUDED_DIRS)
        ]
        assert len(matches) == 0, \
            f"Found {len(matches)} active references to devforgeai-ideation:\n" + "\n".join(matches[:10])

    def test_should_have_zero_matches_in_active_claude_code(self):
        result = subprocess.run(
            ["grep", "-r", "--include=*.md", "--include=*.py", "--include=*.yaml",
             "devforgeai-ideation", os.path.join(PROJECT_ROOT, ".claude")],
            capture_output=True, text=True
        )
        matches = [
            line for line in result.stdout.strip().split("\n")
            if line and not any(excl in line for excl in EXCLUDED_DIRS)
        ]
        assert len(matches) == 0, \
            f"Found {len(matches)} active references to devforgeai-ideation in .claude/"
