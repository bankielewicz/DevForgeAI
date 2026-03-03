"""
Test: AC#2 - SKILL.md Name Field Updated
Story: STORY-440
Generated: 2026-02-18

Verifies SKILL.md YAML frontmatter has name: designing-systems
and internal references use the new name.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_MD_PATH = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "designing-systems", "SKILL.md"
)
README_PATH = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "designing-systems", "README.md"
)


def _read_file(path):
    """Helper to read file content or skip if missing."""
    if not os.path.isfile(path):
        pytest.skip(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestAC2SkillMdUpdated:
    """AC#2: SKILL.md name field updated to designing-systems."""

    def test_should_have_name_designing_systems_in_frontmatter(self):
        """Arrange: SKILL.md content. Act: Parse frontmatter. Assert: name: designing-systems."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(r"^name:\s*designing-systems\s*$", content, re.MULTILINE), (
            "SKILL.md frontmatter does not contain 'name: designing-systems'"
        )

    def test_should_not_have_old_name_in_frontmatter(self):
        """Arrange: SKILL.md content. Act: Search frontmatter. Assert: no devforgeai-architecture."""
        content = _read_file(SKILL_MD_PATH)
        assert not re.search(r"^name:\s*devforgeai-architecture\s*$", content, re.MULTILINE), (
            "SKILL.md frontmatter still contains old name 'devforgeai-architecture'"
        )

    def test_should_not_have_old_name_in_body(self):
        """Arrange: SKILL.md content. Act: Search body. Assert: no devforgeai-architecture refs."""
        content = _read_file(SKILL_MD_PATH)
        # Skip frontmatter for body search
        parts = content.split("---", 2)
        body = parts[2] if len(parts) >= 3 else content
        assert "devforgeai-architecture" not in body, (
            "SKILL.md body still references 'devforgeai-architecture'"
        )

    def test_should_have_readme_with_new_name(self):
        """Arrange: README.md in new dir. Act: Check title. Assert: references designing-systems."""
        content = _read_file(README_PATH)
        assert "designing-systems" in content.lower(), (
            "README.md does not reference 'designing-systems'"
        )
