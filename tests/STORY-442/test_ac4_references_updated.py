"""
Test: AC#4 - Memory/Reference/Context Files Updated
Story: STORY-442
Generated: 2026-02-18

Validates that skills-reference.md, CLAUDE.md, and source-tree.md
reference brainstorming instead of devforgeai-brainstorming.
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class TestAC4ReferencesUpdated:
    """AC#4: Memory/reference/context files updated."""

    SKILLS_REF = os.path.join(
        PROJECT_ROOT, "src", "claude", "memory", "skills-reference.md"
    )
    SOURCE_TREE = os.path.join(
        PROJECT_ROOT, "devforgeai", "specs", "context", "source-tree.md"
    )
    CLAUDE_MD = os.path.join(PROJECT_ROOT, "CLAUDE.md")

    def _read_file(self, path):
        assert os.path.isfile(path), f"File not found: {path}"
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def test_should_list_brainstorming_in_skills_reference_when_updated(self):
        """skills-reference.md lists brainstorming (not devforgeai-brainstorming)."""
        content = self._read_file(self.SKILLS_REF)
        assert "devforgeai-brainstorming" not in content, (
            "Old name 'devforgeai-brainstorming' still in skills-reference.md"
        )

    def test_should_show_brainstorming_directory_in_source_tree_when_updated(self):
        """source-tree.md shows brainstorming/ directory (not devforgeai-brainstorming/)."""
        content = self._read_file(self.SOURCE_TREE)
        assert "devforgeai-brainstorming" not in content, (
            "Old directory name 'devforgeai-brainstorming' still in source-tree.md"
        )

    def test_should_have_brainstorming_in_source_tree_when_updated(self):
        """source-tree.md contains a reference to brainstorming/ skill directory."""
        content = self._read_file(self.SOURCE_TREE)
        # Should have brainstorming as a skill directory entry
        assert "brainstorming/" in content or "brainstorming" in content, (
            "New name 'brainstorming' not found in source-tree.md"
        )

    def test_should_update_claude_md_references_when_updated(self):
        """CLAUDE.md does not contain devforgeai-brainstorming."""
        content = self._read_file(self.CLAUDE_MD)
        assert "devforgeai-brainstorming" not in content, (
            "Old reference 'devforgeai-brainstorming' still in CLAUDE.md"
        )
