"""
Test: AC#3 - Command Files Updated
Story: STORY-440
Generated: 2026-02-18

Verifies command files invoke designing-systems instead of devforgeai-architecture.
"""
import os
import glob
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COMMANDS_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "commands")


def _read_file(path):
    if not os.path.isfile(path):
        pytest.skip(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestAC3CommandsUpdated:
    """AC#3: Command files reference designing-systems, not devforgeai-architecture."""

    def test_should_have_designing_systems_in_create_epic(self):
        """Arrange: create-epic.md. Act: Search. Assert: designing-systems referenced."""
        content = _read_file(os.path.join(COMMANDS_DIR, "create-epic.md"))
        assert "designing-systems" in content, (
            "create-epic.md does not reference 'designing-systems'"
        )

    def test_should_not_have_old_name_in_create_epic(self):
        """Arrange: create-epic.md. Act: Search. Assert: no devforgeai-architecture."""
        content = _read_file(os.path.join(COMMANDS_DIR, "create-epic.md"))
        assert "devforgeai-architecture" not in content, (
            "create-epic.md still references 'devforgeai-architecture'"
        )

    def test_should_have_designing_systems_in_create_context(self):
        """Arrange: create-context.md. Act: Search. Assert: designing-systems referenced."""
        content = _read_file(os.path.join(COMMANDS_DIR, "create-context.md"))
        assert "designing-systems" in content, (
            "create-context.md does not reference 'designing-systems'"
        )

    def test_should_not_have_old_name_in_create_context(self):
        """Arrange: create-context.md. Act: Search. Assert: no devforgeai-architecture."""
        content = _read_file(os.path.join(COMMANDS_DIR, "create-context.md"))
        assert "devforgeai-architecture" not in content, (
            "create-context.md still references 'devforgeai-architecture'"
        )

    def test_should_not_have_old_name_in_any_command_file(self):
        """Arrange: All command .md files. Act: Grep. Assert: zero matches for old name."""
        if not os.path.isdir(COMMANDS_DIR):
            pytest.skip(f"Commands directory not found: {COMMANDS_DIR}")
        violations = []
        for md_file in glob.glob(os.path.join(COMMANDS_DIR, "*.md")):
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            if "devforgeai-architecture" in content:
                violations.append(os.path.basename(md_file))
        assert not violations, (
            f"Command files still reference 'devforgeai-architecture': {violations}"
        )
