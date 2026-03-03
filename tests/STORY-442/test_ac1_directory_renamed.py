"""
Test: AC#1 - Skill Directory Renamed
Story: STORY-442
Generated: 2026-02-18

Validates that devforgeai-brainstorming directory is renamed to brainstorming
in both src/ and .claude/ paths, with all files preserved.
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class TestAC1DirectoryRenamed:
    """AC#1: Skill directory renamed from devforgeai-brainstorming to brainstorming."""

    # --- Arrange ---
    NEW_SRC_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "brainstorming")
    OLD_SRC_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-brainstorming")
    NEW_OPS_DIR = os.path.join(PROJECT_ROOT, ".claude", "skills", "brainstorming")
    OLD_OPS_DIR = os.path.join(PROJECT_ROOT, ".claude", "skills", "devforgeai-brainstorming")

    # --- Act & Assert ---

    def test_should_have_new_src_directory_when_rename_applied(self):
        """New directory exists at src/claude/skills/brainstorming/."""
        assert os.path.isdir(self.NEW_SRC_DIR), (
            f"Expected new directory at {self.NEW_SRC_DIR}"
        )

    def test_should_not_have_old_src_directory_when_rename_applied(self):
        """Old directory src/claude/skills/devforgeai-brainstorming/ no longer exists."""
        assert not os.path.exists(self.OLD_SRC_DIR), (
            f"Old directory should not exist at {self.OLD_SRC_DIR}"
        )

    def test_should_have_new_operational_directory_when_rename_applied(self):
        """New directory exists at .claude/skills/brainstorming/."""
        assert os.path.isdir(self.NEW_OPS_DIR), (
            f"Expected new operational directory at {self.NEW_OPS_DIR}"
        )

    def test_should_not_have_old_operational_directory_when_rename_applied(self):
        """Old directory .claude/skills/devforgeai-brainstorming/ no longer exists."""
        assert not os.path.exists(self.OLD_OPS_DIR), (
            f"Old operational directory should not exist at {self.OLD_OPS_DIR}"
        )

    def test_should_have_skillmd_in_new_src_directory_when_rename_applied(self):
        """SKILL.md exists in new src directory."""
        skill_md = os.path.join(self.NEW_SRC_DIR, "SKILL.md")
        assert os.path.isfile(skill_md), (
            f"Expected SKILL.md at {skill_md}"
        )

    def test_should_preserve_all_files_when_rename_applied(self):
        """All files present in new location (minimum 2: SKILL.md + assets/)."""
        assert os.path.isdir(self.NEW_SRC_DIR), f"Directory missing: {self.NEW_SRC_DIR}"
        file_count = sum(
            len(files) for _, _, files in os.walk(self.NEW_SRC_DIR)
        )
        assert file_count >= 2, (
            f"Expected at least 2 files in {self.NEW_SRC_DIR}, found {file_count}"
        )

    def test_should_have_assets_directory_when_rename_applied(self):
        """Assets directory preserved in new location."""
        assets_dir = os.path.join(self.NEW_SRC_DIR, "assets")
        assert os.path.isdir(assets_dir), (
            f"Expected assets directory at {assets_dir}"
        )
