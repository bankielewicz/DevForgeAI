"""AC#4: Positioning Matrix Dimensions
Story: STORY-536
Tests that positioning matrix has required dimensions per competitor.
"""
import re
import pytest


class TestMatrixRequiredDimensions:
    """Each competitor must have: name, category, strengths, weaknesses, position summary, differentiation."""

    def test_subagent_specifies_name_dimension(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        assert re.search(r"(?i)\bname\b", subagent_content), (
            "Subagent must specify 'name' as a positioning matrix dimension"
        )

    def test_subagent_specifies_category_dimension(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        assert re.search(r"(?i)\bcategory\b", subagent_content), (
            "Subagent must specify 'category' as a positioning matrix dimension"
        )

    def test_subagent_specifies_strengths_dimension(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        assert re.search(r"(?i)\bstrength", subagent_content), (
            "Subagent must specify 'strengths' as a positioning matrix dimension"
        )

    def test_subagent_specifies_weaknesses_dimension(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        assert re.search(r"(?i)\bweakness", subagent_content), (
            "Subagent must specify 'weaknesses' as a positioning matrix dimension"
        )

    def test_subagent_specifies_market_position_summary(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        assert re.search(r"(?i)market\s+position\s+summary", subagent_content), (
            "Subagent must specify 'market position summary' as a positioning matrix dimension"
        )

    def test_subagent_specifies_differentiation_dimension(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        assert re.search(r"(?i)\bdifferentiation\b", subagent_content), (
            "Subagent must specify 'differentiation' as a positioning matrix dimension"
        )


class TestMatrixMinimumCounts:
    """Verify minimum count requirements are documented."""

    def test_min_one_strength_documented(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        # Must mention minimum 1 or "at least 1" for strengths
        assert re.search(r"(?i)(min(imum)?\s*(of\s*)?1|at\s+least\s+(one|1)).{0,30}strength", subagent_content) or \
               re.search(r"(?i)strength.{0,30}(min(imum)?\s*(of\s*)?1|at\s+least\s+(one|1))", subagent_content), (
            "Subagent must document minimum 1 strength per competitor"
        )

    def test_min_one_weakness_documented(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        assert re.search(r"(?i)(min(imum)?\s*(of\s*)?1|at\s+least\s+(one|1)).{0,30}weakness", subagent_content) or \
               re.search(r"(?i)weakness.{0,30}(min(imum)?\s*(of\s*)?1|at\s+least\s+(one|1))", subagent_content), (
            "Subagent must document minimum 1 weakness per competitor"
        )

    def test_min_one_differentiation_documented(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        assert re.search(r"(?i)(min(imum)?\s*(of\s*)?1|at\s+least\s+(one|1)).{0,30}differentiation", subagent_content) or \
               re.search(r"(?i)differentiation.{0,30}(min(imum)?\s*(of\s*)?1|at\s+least\s+(one|1))", subagent_content), (
            "Subagent must document minimum 1 differentiation per competitor"
        )
