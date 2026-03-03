"""
Test: AC#7 - Dual-Path Sync (src/ and .claude/)
Story: STORY-440
Generated: 2026-02-18

Verifies src/ and .claude/ designing-systems directories contain identical content.
"""
import os
import filecmp
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "designing-systems")
OPS_DIR = os.path.join(PROJECT_ROOT, ".claude", "skills", "designing-systems")


def _list_files(directory):
    """List all files relative to directory root."""
    result = []
    if not os.path.isdir(directory):
        return result
    for root, _, files in os.walk(directory):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), directory)
            result.append(rel)
    return sorted(result)


class TestAC7DualPathSync:
    """AC#7: src/ and .claude/ designing-systems directories match."""

    def test_should_have_both_directories(self):
        """Arrange: Both paths. Act: Check existence. Assert: Both exist."""
        assert os.path.isdir(SRC_DIR), f"Source directory missing: {SRC_DIR}"
        assert os.path.isdir(OPS_DIR), f"Operational directory missing: {OPS_DIR}"

    def test_should_have_same_file_list(self):
        """Arrange: Both dirs. Act: List files. Assert: Identical file sets."""
        if not os.path.isdir(SRC_DIR) or not os.path.isdir(OPS_DIR):
            pytest.skip("One or both directories missing")
        src_files = _list_files(SRC_DIR)
        ops_files = _list_files(OPS_DIR)
        assert src_files == ops_files, (
            f"File lists differ.\n"
            f"Only in src/: {set(src_files) - set(ops_files)}\n"
            f"Only in .claude/: {set(ops_files) - set(src_files)}"
        )

    def test_should_have_identical_content(self):
        """Arrange: Both dirs. Act: Compare files. Assert: Content matches."""
        if not os.path.isdir(SRC_DIR) or not os.path.isdir(OPS_DIR):
            pytest.skip("One or both directories missing")
        comparison = filecmp.dircmp(SRC_DIR, OPS_DIR)
        mismatches = []
        self._collect_mismatches(comparison, mismatches)
        assert not mismatches, (
            f"Content differs between src/ and .claude/:\n"
            + "\n".join(f"  - {m}" for m in mismatches)
        )

    def _collect_mismatches(self, dcmp, results, prefix=""):
        """Recursively collect file mismatches."""
        for name in dcmp.diff_files:
            results.append(os.path.join(prefix, name))
        for name in dcmp.left_only:
            results.append(f"{os.path.join(prefix, name)} (only in src/)")
        for name in dcmp.right_only:
            results.append(f"{os.path.join(prefix, name)} (only in .claude/)")
        for sub_name, sub_dcmp in dcmp.subdirs.items():
            self._collect_mismatches(sub_dcmp, results, os.path.join(prefix, sub_name))

    def test_should_not_have_old_directories(self):
        """Arrange: Old paths. Act: Check. Assert: Neither old dir exists."""
        old_src = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture")
        old_ops = os.path.join(PROJECT_ROOT, ".claude", "skills", "devforgeai-architecture")
        assert not os.path.exists(old_src), f"Old src/ directory still exists: {old_src}"
        assert not os.path.exists(old_ops), f"Old .claude/ directory still exists: {old_ops}"
