"""AC#8: Dual-Path Sync (src/ and .claude/)."""
import os
import filecmp

import pytest

from conftest import SRC_NEW, OPS_NEW, SRC_OLD, OPS_OLD


class TestAC8DualPathSync:
    """AC#8: src/ and .claude/ paths are synchronized."""

    def test_should_have_both_new_directories(self):
        assert os.path.isdir(SRC_NEW), f"Missing {SRC_NEW}"
        assert os.path.isdir(OPS_NEW), f"Missing {OPS_NEW}"

    def test_should_not_have_old_directories_in_either_path(self):
        assert not os.path.isdir(SRC_OLD), f"Old dir still exists: {SRC_OLD}"
        assert not os.path.isdir(OPS_OLD), f"Old dir still exists: {OPS_OLD}"

    def test_should_have_identical_content_between_paths(self):
        if not os.path.isdir(SRC_NEW) or not os.path.isdir(OPS_NEW):
            pytest.skip("Directories don't exist yet (pre-implementation)")
        comparison = filecmp.dircmp(SRC_NEW, OPS_NEW)
        assert not comparison.diff_files, f"Files differ: {comparison.diff_files}"
        assert not comparison.left_only, f"Only in src/: {comparison.left_only}"
        assert not comparison.right_only, f"Only in .claude/: {comparison.right_only}"
