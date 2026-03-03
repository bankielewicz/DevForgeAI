"""
Test: AC#5 - Context Files Updated
Story: STORY-440
Generated: 2026-02-18

Verifies coding-standards.md and source-tree.md use designing-systems naming.
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONTEXT_DIR = os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context")


def _read_file(path):
    if not os.path.isfile(path):
        pytest.skip(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestAC5ContextFilesUpdated:
    """AC#5: Context files updated for gerund naming convention."""

    def test_should_have_designing_systems_in_source_tree(self):
        """Arrange: source-tree.md. Act: Search. Assert: designing-systems/ listed."""
        content = _read_file(os.path.join(CONTEXT_DIR, "source-tree.md"))
        assert "designing-systems" in content, (
            "source-tree.md does not list 'designing-systems'"
        )

    def test_should_not_have_old_skill_dir_in_source_tree(self):
        """Arrange: source-tree.md. Act: Search directory listing. Assert: no devforgeai-architecture/."""
        content = _read_file(os.path.join(CONTEXT_DIR, "source-tree.md"))
        # Check for the directory entry specifically
        assert "devforgeai-architecture/" not in content, (
            "source-tree.md still lists 'devforgeai-architecture/' directory"
        )

    def test_should_have_gerund_pattern_in_coding_standards(self):
        """Arrange: coding-standards.md. Act: Search naming section. Assert: gerund examples present."""
        content = _read_file(os.path.join(CONTEXT_DIR, "coding-standards.md"))
        assert "designing-systems" in content or "designing-" in content, (
            "coding-standards.md does not reference gerund naming with 'designing-' pattern"
        )

    def test_should_not_have_old_name_example_in_coding_standards(self):
        """Arrange: coding-standards.md. Act: Search. Assert: no devforgeai-architecture as example."""
        content = _read_file(os.path.join(CONTEXT_DIR, "coding-standards.md"))
        assert "devforgeai-architecture" not in content, (
            "coding-standards.md still uses 'devforgeai-architecture' as example"
        )
