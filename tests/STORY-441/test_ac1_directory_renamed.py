"""AC#1: Skill Directory Renamed.

Tests that discovering-requirements directory exists and devforgeai-ideation is removed.
All tests MUST FAIL before implementation (TDD Red phase).
"""
import os

from conftest import SRC_NEW, SRC_OLD, OPS_NEW, OPS_OLD


class TestAC1DirectoryRenamed:
    """AC#1: Verify directory rename from devforgeai-ideation to discovering-requirements."""

    def test_should_have_new_src_directory_when_renamed(self):
        assert os.path.isdir(SRC_NEW), f"Expected new directory at {SRC_NEW}"

    def test_should_not_have_old_src_directory_when_renamed(self):
        assert not os.path.isdir(SRC_OLD), f"Old directory should not exist at {SRC_OLD}"

    def test_should_have_new_operational_directory_when_renamed(self):
        assert os.path.isdir(OPS_NEW), f"Expected operational directory at {OPS_NEW}"

    def test_should_not_have_old_operational_directory_when_renamed(self):
        assert not os.path.isdir(OPS_OLD), f"Old operational directory should not exist at {OPS_OLD}"

    def test_should_have_skillmd_in_new_directory_when_renamed(self):
        assert os.path.isfile(os.path.join(SRC_NEW, "SKILL.md")), "SKILL.md must exist in discovering-requirements/"

    def test_should_have_references_dir_in_new_directory_when_renamed(self):
        assert os.path.isdir(os.path.join(SRC_NEW, "references")), "references/ must exist in discovering-requirements/"
