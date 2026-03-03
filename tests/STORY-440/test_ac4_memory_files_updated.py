"""
Test: AC#4 - Memory/Reference Files Updated
Story: STORY-440
Generated: 2026-02-18

Verifies skills-reference.md and CLAUDE.md reference designing-systems.
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _read_file(path):
    if not os.path.isfile(path):
        pytest.skip(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestAC4MemoryFilesUpdated:
    """AC#4: Memory and reference files list designing-systems."""

    def test_should_have_designing_systems_in_skills_reference(self):
        """Arrange: skills-reference.md. Act: Search. Assert: designing-systems listed."""
        path = os.path.join(PROJECT_ROOT, "src", "claude", "memory", "skills-reference.md")
        content = _read_file(path)
        assert "designing-systems" in content, (
            "skills-reference.md does not list 'designing-systems'"
        )

    def test_should_not_have_old_name_in_skills_reference(self):
        """Arrange: skills-reference.md. Act: Search. Assert: no devforgeai-architecture."""
        path = os.path.join(PROJECT_ROOT, "src", "claude", "memory", "skills-reference.md")
        content = _read_file(path)
        assert "devforgeai-architecture" not in content, (
            "skills-reference.md still references 'devforgeai-architecture'"
        )

    def test_should_have_designing_systems_in_claude_md(self):
        """Arrange: CLAUDE.md. Act: Search. Assert: designing-systems referenced."""
        path = os.path.join(PROJECT_ROOT, "CLAUDE.md")
        content = _read_file(path)
        assert "designing-systems" in content, (
            "CLAUDE.md does not reference 'designing-systems'"
        )

    def test_should_not_have_old_name_in_claude_md_active_refs(self):
        """Arrange: CLAUDE.md. Act: Search active sections. Assert: no devforgeai-architecture."""
        path = os.path.join(PROJECT_ROOT, "CLAUDE.md")
        content = _read_file(path)
        # Exclude historical/comment sections - check for active skill references
        assert "devforgeai-architecture" not in content, (
            "CLAUDE.md still contains 'devforgeai-architecture' references"
        )
