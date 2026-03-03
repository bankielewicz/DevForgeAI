"""
STORY-506: ADR-025 Acceptance and Source-Tree Update
Tests for AC#1-AC#5 - Documentation story verification

TDD Red Phase: All tests should FAIL before implementation.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ADR_PATH = os.path.join(PROJECT_ROOT, "devforgeai", "specs", "adrs", "ADR-025-qa-diff-regression-detection.md")
SOURCE_TREE_PATH = os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context", "source-tree.md")


@pytest.fixture
def adr_content():
    """Read ADR-025 file content."""
    with open(ADR_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def source_tree_content():
    """Read source-tree.md file content."""
    with open(SOURCE_TREE_PATH, "r", encoding="utf-8") as f:
        return f.read()


# === AC#1: ADR-025 Status Updated from Proposed to Accepted ===

class TestAC1_ADRStatusUpdate:
    """AC#1: ADR-025 status should be Accepted."""

    def test_adr025_status_is_accepted(self, adr_content):
        """ADR-025 status field must be 'Accepted', not 'Proposed'."""
        assert "**Status:** Accepted" in adr_content, (
            "ADR-025 status should be 'Accepted'"
        )

    def test_adr025_status_not_proposed(self, adr_content):
        """ADR-025 should no longer show 'Proposed' status."""
        # After update, the status line should not contain Proposed
        status_match = re.search(r"\*\*Status:\*\*\s+(\w+)", adr_content)
        assert status_match is not None, "Status field not found in ADR-025"
        assert status_match.group(1) != "Proposed", (
            "ADR-025 status should not be 'Proposed'"
        )

    def test_adr025_has_acceptance_date(self, adr_content):
        """ADR-025 must have an acceptance date in ISO 8601 format."""
        # Look for a line like "**Acceptance Date:** 2026-02-27"
        assert re.search(
            r"\*\*Acceptance Date:\*\*\s+\d{4}-\d{2}-\d{2}", adr_content
        ), "ADR-025 must contain an acceptance date in YYYY-MM-DD format"


# === AC#2: source-tree.md Documents devforgeai/qa/snapshots/ ===

class TestAC2_SnapshotDirectoryEntry:
    """AC#2: source-tree.md must document devforgeai/qa/snapshots/ directory."""

    def test_snapshots_directory_in_source_tree(self, source_tree_content):
        """source-tree.md must contain devforgeai/qa/snapshots/ entry."""
        assert "snapshots/" in source_tree_content, (
            "source-tree.md must document the snapshots/ directory"
        )

    def test_snapshots_described_as_root_storage(self, source_tree_content):
        """Snapshots directory must be described as root snapshot storage."""
        # Look for snapshot description near the snapshots entry
        assert re.search(
            r"snapshots/.*(?:snapshot|integrity|checksum)",
            source_tree_content,
            re.IGNORECASE | re.DOTALL,
        ), "snapshots/ must be described with its storage purpose"


# === AC#3: {STORY_ID}/ Subdirectory Pattern ===

class TestAC3_StoryIDSubdirectory:
    """AC#3: source-tree.md must document {STORY_ID}/ pattern."""

    def test_story_id_pattern_documented(self, source_tree_content):
        """{STORY_ID}/ subdirectory pattern must appear in source-tree.md."""
        assert "{STORY_ID}/" in source_tree_content or "{STORY-ID}/" in source_tree_content, (
            "source-tree.md must document the {STORY_ID}/ subdirectory pattern"
        )

    def test_story_id_has_isolation_description(self, source_tree_content):
        """The {STORY_ID}/ pattern must describe per-story isolation near snapshots section."""
        # Find the snapshots section first, then check for STORY_ID pattern nearby
        snapshot_pos = source_tree_content.find("snapshots/")
        assert snapshot_pos != -1, "snapshots/ section must exist first"
        # Look within 500 chars after snapshots/ for the STORY_ID pattern with description
        nearby = source_tree_content[snapshot_pos:snapshot_pos + 500]
        assert re.search(
            r"STORY.ID.*(?:per-story|isolation|individual|separate)",
            nearby,
            re.IGNORECASE | re.DOTALL,
        ), "{STORY_ID}/ must describe per-story isolation purpose near snapshots section"


# === AC#4: red-phase-checksums.json Documented ===

class TestAC4_ChecksumsFile:
    """AC#4: source-tree.md must document red-phase-checksums.json."""

    def test_checksums_file_documented(self, source_tree_content):
        """red-phase-checksums.json must appear in source-tree.md."""
        assert "red-phase-checksums.json" in source_tree_content, (
            "source-tree.md must document red-phase-checksums.json"
        )

    def test_checksums_purpose_described(self, source_tree_content):
        """red-phase-checksums.json must describe its checksum/integrity purpose."""
        assert re.search(
            r"red-phase-checksums\.json.*(?:checksum|SHA|integrity|Red.phase)",
            source_tree_content,
            re.IGNORECASE | re.DOTALL,
        ), "red-phase-checksums.json must describe its purpose"


# === AC#5: ADR-025 Cross-Reference in source-tree.md ===

class TestAC5_ADRCrossReference:
    """AC#5: source-tree.md snapshot section must cross-reference ADR-025."""

    def test_adr025_referenced_in_source_tree(self, source_tree_content):
        """ADR-025 must be referenced in source-tree.md."""
        assert "ADR-025" in source_tree_content, (
            "source-tree.md must include a cross-reference to ADR-025"
        )

    def test_adr025_near_snapshot_section(self, source_tree_content):
        """ADR-025 reference must appear near the snapshot directory section."""
        # Find snapshot entry and ADR-025 reference - they should be within 500 chars
        snapshot_pos = source_tree_content.find("snapshots/")
        adr_pos = source_tree_content.find("ADR-025")
        if snapshot_pos == -1:
            pytest.fail("snapshots/ not found in source-tree.md")
        if adr_pos == -1:
            pytest.fail("ADR-025 not found in source-tree.md")
        distance = abs(adr_pos - snapshot_pos)
        assert distance < 500, (
            f"ADR-025 reference should be near snapshots/ section (distance: {distance} chars)"
        )
