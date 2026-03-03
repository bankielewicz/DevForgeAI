"""
Test: AC#6 - Dual-Path Sync (src/ and .claude/)
Story: STORY-442
Generated: 2026-02-18

Validates that both src/claude/skills/brainstorming/ and .claude/skills/brainstorming/
exist with identical content, and old directories are removed from both paths.
"""
import os
import filecmp
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class TestAC6DualPathSync:
    """AC#6: Dual-path sync - src/ and .claude/ directories match."""

    SRC_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "brainstorming")
    OPS_DIR = os.path.join(PROJECT_ROOT, ".claude", "skills", "brainstorming")
    OLD_SRC_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-brainstorming")
    OLD_OPS_DIR = os.path.join(PROJECT_ROOT, ".claude", "skills", "devforgeai-brainstorming")

    def test_should_have_src_brainstorming_directory_when_sync_complete(self):
        """src/claude/skills/brainstorming/ exists."""
        assert os.path.isdir(self.SRC_DIR), (
            f"Source directory missing: {self.SRC_DIR}"
        )

    def test_should_have_ops_brainstorming_directory_when_sync_complete(self):
        """.claude/skills/brainstorming/ exists."""
        assert os.path.isdir(self.OPS_DIR), (
            f"Operational directory missing: {self.OPS_DIR}"
        )

    def test_should_not_have_old_src_directory_when_sync_complete(self):
        """Old src/claude/skills/devforgeai-brainstorming/ removed."""
        assert not os.path.exists(self.OLD_SRC_DIR), (
            f"Old source directory still exists: {self.OLD_SRC_DIR}"
        )

    def test_should_not_have_old_ops_directory_when_sync_complete(self):
        """Old .claude/skills/devforgeai-brainstorming/ removed."""
        assert not os.path.exists(self.OLD_OPS_DIR), (
            f"Old operational directory still exists: {self.OLD_OPS_DIR}"
        )

    def test_should_have_identical_content_when_sync_complete(self):
        """Both directories contain identical files."""
        assert os.path.isdir(self.SRC_DIR), f"Source missing: {self.SRC_DIR}"
        assert os.path.isdir(self.OPS_DIR), f"Ops missing: {self.OPS_DIR}"

        comparison = filecmp.dircmp(self.SRC_DIR, self.OPS_DIR)
        diff_files = comparison.diff_files
        left_only = comparison.left_only
        right_only = comparison.right_only

        assert not diff_files, f"Files differ between paths: {diff_files}"
        assert not left_only, f"Files only in src/: {left_only}"
        assert not right_only, f"Files only in .claude/: {right_only}"

    def test_should_have_skillmd_in_both_paths_when_sync_complete(self):
        """SKILL.md exists in both src/ and .claude/ paths."""
        src_skill = os.path.join(self.SRC_DIR, "SKILL.md")
        ops_skill = os.path.join(self.OPS_DIR, "SKILL.md")
        assert os.path.isfile(src_skill), f"SKILL.md missing in src: {src_skill}"
        assert os.path.isfile(ops_skill), f"SKILL.md missing in ops: {ops_skill}"
