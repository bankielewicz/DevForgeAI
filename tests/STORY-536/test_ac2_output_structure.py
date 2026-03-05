"""AC#2: Competitive Analysis Output
Story: STORY-536
Tests that competitive-analysis.md has required sections.
"""
import os
import re
import pytest


class TestOutputFileExists:
    """Verify output file exists at correct path."""

    def test_output_file_exists(self, output_path):
        assert os.path.isfile(output_path), (
            f"competitive-analysis.md not found at {output_path}"
        )


class TestOutputContainsPositioningMatrix:
    """Verify output contains positioning matrix section."""

    def test_has_positioning_matrix_heading(self, output_content):
        assert output_content, "Output file is empty or missing"
        assert re.search(r"(?i)##?\s+positioning\s+matrix", output_content), (
            "Output must contain a 'Positioning Matrix' section heading"
        )


class TestOutputContainsCompetitorProfiles:
    """Verify per-competitor strengths and weaknesses."""

    def test_has_strengths_section(self, output_content):
        assert output_content, "Output file is empty or missing"
        assert re.search(r"(?i)strength", output_content), (
            "Output must contain strengths for competitors"
        )

    def test_has_weaknesses_section(self, output_content):
        assert output_content, "Output file is empty or missing"
        assert re.search(r"(?i)weakness", output_content), (
            "Output must contain weaknesses for competitors"
        )


class TestOutputContainsDifferentiation:
    """Verify differentiation opportunities section."""

    def test_has_differentiation_section(self, output_content):
        assert output_content, "Output file is empty or missing"
        assert re.search(r"(?i)differentiation", output_content), (
            "Output must contain differentiation opportunities"
        )
