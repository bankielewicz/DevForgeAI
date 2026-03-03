"""Test AC#4: Reference Files for Progressive Disclosure.

Story: STORY-465
Validates that the 4 required reference files exist, are non-empty,
and are under 1500 lines each.
"""
import pytest
from pathlib import Path


REQUIRED_REFERENCES = [
    "adhd-adaptation-framework.md",
    "confidence-assessment-workflow.md",
    "work-style-questionnaire.md",
    "plan-calibration-engine.md",
]


class TestReferenceFilesExist:
    """Tests for reference file existence."""

    @pytest.mark.parametrize("filename", REQUIRED_REFERENCES)
    def test_should_exist(self, references_dir, filename):
        """Each required reference file must exist in the references/ directory."""
        filepath = references_dir / filename
        assert filepath.exists(), (
            f"Reference file not found: {filepath}. "
            f"The file '{filename}' must be created in the references/ directory."
        )

    def test_should_have_all_four_files(self, references_dir):
        """All 4 reference files must be present."""
        missing = [
            f for f in REQUIRED_REFERENCES
            if not (references_dir / f).exists()
        ]
        assert len(missing) == 0, (
            f"Missing {len(missing)} reference files: {missing}"
        )


class TestReferenceFileContent:
    """Tests for reference file content quality."""

    @pytest.mark.parametrize("filename", REQUIRED_REFERENCES)
    def test_should_be_non_empty(self, references_dir, filename):
        """Each reference file must contain substantive content."""
        filepath = references_dir / filename
        content = filepath.read_text(encoding="utf-8")
        assert len(content.strip()) > 50, (
            f"Reference file '{filename}' appears empty or contains only "
            f"minimal content ({len(content.strip())} chars)."
        )

    @pytest.mark.parametrize("filename", REQUIRED_REFERENCES)
    def test_should_be_under_1500_lines(self, references_dir, filename):
        """Each reference file must be under 1500 lines."""
        filepath = references_dir / filename
        content = filepath.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
        assert line_count < 1500, (
            f"Reference file '{filename}' has {line_count} lines, "
            f"exceeds 1500 line limit."
        )
