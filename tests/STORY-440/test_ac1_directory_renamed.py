"""
Test: AC#1 - Skill Directory Renamed
Story: STORY-440
Generated: 2026-02-18

Verifies devforgeai-architecture directory is renamed to designing-systems
in both src/ and .claude/ paths, and old directory no longer exists.
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class TestAC1DirectoryRenamed:
    """AC#1: Skill directory renamed from devforgeai-architecture to designing-systems."""

    # --- New directory exists ---

    def test_should_have_designing_systems_dir_in_src(self):
        """Arrange: src/ skill tree. Act: Check path. Assert: designing-systems/ exists."""
        new_dir = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "designing-systems")
        assert os.path.isdir(new_dir), (
            f"Expected new directory at {new_dir} but it does not exist"
        )

    def test_should_have_designing_systems_dir_in_operational(self):
        """Arrange: .claude/ skill tree. Act: Check path. Assert: designing-systems/ exists."""
        new_dir = os.path.join(PROJECT_ROOT, ".claude", "skills", "designing-systems")
        assert os.path.isdir(new_dir), (
            f"Expected operational directory at {new_dir} but it does not exist"
        )

    # --- Old directory removed ---

    def test_should_not_have_old_dir_in_src(self):
        """Arrange: src/ skill tree. Act: Check old path. Assert: devforgeai-architecture/ gone."""
        old_dir = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture")
        assert not os.path.exists(old_dir), (
            f"Old directory still exists at {old_dir} - should be removed after rename"
        )

    def test_should_not_have_old_dir_in_operational(self):
        """Arrange: .claude/ skill tree. Act: Check old path. Assert: devforgeai-architecture/ gone."""
        old_dir = os.path.join(PROJECT_ROOT, ".claude", "skills", "devforgeai-architecture")
        assert not os.path.exists(old_dir), (
            f"Old operational directory still exists at {old_dir} - should be removed after rename"
        )

    # --- SKILL.md present in new location ---

    def test_should_have_skillmd_in_new_src_dir(self):
        """Arrange: New src dir. Act: Check SKILL.md. Assert: File exists."""
        skill_md = os.path.join(
            PROJECT_ROOT, "src", "claude", "skills", "designing-systems", "SKILL.md"
        )
        assert os.path.isfile(skill_md), (
            f"SKILL.md not found at {skill_md}"
        )

    # --- File count preserved ---

    def test_should_preserve_file_count_in_new_directory(self):
        """Arrange: New directory. Act: Count files recursively. Assert: >= 10 files present."""
        new_dir = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "designing-systems")
        if not os.path.isdir(new_dir):
            pytest.skip("New directory does not exist yet")
        file_count = sum(len(files) for _, _, files in os.walk(new_dir))
        assert file_count >= 10, (
            f"Expected at least 10 files in new directory, found {file_count}"
        )
