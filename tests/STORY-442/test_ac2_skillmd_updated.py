"""
Test: AC#2 - SKILL.md Name Field Updated
Story: STORY-442
Generated: 2026-02-18

Validates that SKILL.md YAML frontmatter name field is updated to brainstorming.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class TestAC2SkillmdUpdated:
    """AC#2: SKILL.md name field updated to brainstorming."""

    SKILL_MD_PATH = os.path.join(
        PROJECT_ROOT, "src", "claude", "skills", "brainstorming", "SKILL.md"
    )

    def _read_skill_md(self):
        """Helper to read SKILL.md content."""
        assert os.path.isfile(self.SKILL_MD_PATH), (
            f"SKILL.md not found at {self.SKILL_MD_PATH}"
        )
        with open(self.SKILL_MD_PATH, "r", encoding="utf-8") as f:
            return f.read()

    def test_should_have_name_brainstorming_in_frontmatter_when_updated(self):
        """YAML frontmatter contains name: brainstorming (not devforgeai-brainstorming)."""
        content = self._read_skill_md()
        # Extract frontmatter between --- markers
        match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        assert match, "No YAML frontmatter found in SKILL.md"
        frontmatter = match.group(1)
        assert re.search(r"^name:\s*brainstorming\s*$", frontmatter, re.MULTILINE), (
            "Expected 'name: brainstorming' in frontmatter"
        )

    def test_should_not_have_old_name_in_frontmatter_when_updated(self):
        """YAML frontmatter does not contain devforgeai-brainstorming."""
        content = self._read_skill_md()
        match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        assert match, "No YAML frontmatter found in SKILL.md"
        frontmatter = match.group(1)
        assert "devforgeai-brainstorming" not in frontmatter, (
            "Old name 'devforgeai-brainstorming' still in frontmatter"
        )

    def test_should_not_have_old_self_references_when_updated(self):
        """No internal self-references to devforgeai-brainstorming in SKILL.md body."""
        content = self._read_skill_md()
        # Check body (after frontmatter)
        parts = content.split("---", 2)
        body = parts[2] if len(parts) > 2 else content
        assert "devforgeai-brainstorming" not in body, (
            "Old self-reference 'devforgeai-brainstorming' found in SKILL.md body"
        )
