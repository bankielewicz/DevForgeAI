"""
Test: AC#3 - Source-Tree.md Updated to v3.9
Story: STORY-407
Generated: 2026-02-16

Validates that devforgeai/specs/context/source-tree.md version is incremented
to 3.9 and new paths are added.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_TREE_PATH = os.path.join(
    PROJECT_ROOT, "devforgeai", "specs", "context", "source-tree.md"
)


@pytest.fixture(scope="module")
def source_tree_content():
    """Read source-tree.md content."""
    assert os.path.isfile(SOURCE_TREE_PATH), (
        f"source-tree.md not found at {SOURCE_TREE_PATH}"
    )
    with open(SOURCE_TREE_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestVersionUpdate:
    """Tests for version increment from 3.8 to 3.9."""

    def test_should_have_version_3_9(self, source_tree_content):
        """Assert: Version is 3.9."""
        assert re.search(r"(?i)version.*3\.9", source_tree_content), (
            "source-tree.md should be version 3.9"
        )

    def test_should_not_still_be_version_3_8(self, source_tree_content):
        """Assert: Version is no longer 3.8 in the header."""
        # Check the Version line specifically
        version_line = re.search(r"\*\*Version\*\*:.*", source_tree_content)
        assert version_line, "Should have a Version line"
        assert "3.8" not in version_line.group(0), (
            "Version line should no longer show 3.8"
        )


class TestDeadCodeDetectorPaths:
    """Tests for dead-code-detector paths added."""

    def test_should_have_dead_code_detector_agent_path(self, source_tree_content):
        """Assert: dead-code-detector.md path is listed."""
        assert "dead-code-detector.md" in source_tree_content, (
            "source-tree.md should list dead-code-detector.md"
        )

    def test_should_have_entry_point_patterns_path(self, source_tree_content):
        """Assert: entry-point-patterns.md reference path is listed."""
        assert "entry-point-patterns.md" in source_tree_content, (
            "source-tree.md should list entry-point-patterns.md"
        )


class TestCodeSmellCatalogPath:
    """Tests for code-smell-catalog path added."""

    def test_should_have_code_smell_catalog_path(self, source_tree_content):
        """Assert: code-smell-catalog.md path is listed."""
        assert "code-smell-catalog.md" in source_tree_content, (
            "source-tree.md should list code-smell-catalog.md"
        )

    def test_should_show_catalog_under_anti_pattern_scanner(self, source_tree_content):
        """Assert: Catalog path shows under anti-pattern-scanner references."""
        assert re.search(
            r"anti-pattern-scanner.*references.*code-smell-catalog",
            source_tree_content,
            re.DOTALL,
        ), "code-smell-catalog.md should be under anti-pattern-scanner/references/"


class TestTwoStageFilterPath:
    """Tests for two-stage-filter-patterns.md path added."""

    def test_should_have_two_stage_filter_patterns_path(self, source_tree_content):
        """Assert: two-stage-filter-patterns.md path is listed."""
        assert "two-stage-filter-patterns.md" in source_tree_content, (
            "source-tree.md should list two-stage-filter-patterns.md"
        )
