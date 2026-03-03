"""AC#4: Memory/Reference Files Updated."""
import os

from conftest import PROJECT_ROOT


class TestAC4MemoryFilesUpdated:
    """AC#4: Memory files reference discovering-requirements."""

    def test_should_list_discovering_requirements_in_skills_reference(self):
        path = os.path.join(PROJECT_ROOT, "src", "claude", "memory", "skills-reference.md")
        with open(path) as f:
            content = f.read()
        assert "discovering-requirements" in content

    def test_should_not_have_old_name_in_skills_reference(self):
        path = os.path.join(PROJECT_ROOT, "src", "claude", "memory", "skills-reference.md")
        with open(path) as f:
            content = f.read()
        assert "devforgeai-ideation" not in content

    def test_should_not_have_old_name_in_claudemd(self):
        path = os.path.join(PROJECT_ROOT, "CLAUDE.md")
        with open(path) as f:
            content = f.read()
        assert "devforgeai-ideation" not in content
