"""
Test: AC#5 - Boundary and Ambiguous Results Show Comparison Table with Explanation
Story: STORY-552
Generated: 2026-03-06

Validates that the guide defines handling for boundary/ambiguous inputs
including a comparison table with suitability ratings and plain-language
explanation.
"""
import re
import pytest


class TestComparisonTableSection:
    """Verify comparison table section exists for boundary cases."""

    def test_should_contain_comparison_table_section_when_guide_loaded(self, guide_content):
        pattern = re.compile(r'comparison\s+table|boundary|ambiguous', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Guide must contain a comparison table section for boundary cases"
        )

    def test_should_contain_markdown_table_syntax_when_boundary_section_exists(self, guide_content):
        """Verify actual markdown table syntax (pipes and dashes) exists."""
        # Markdown tables use | column | column | format
        pattern = re.compile(r'\|.*\|.*\|')
        assert pattern.search(guide_content), (
            "Guide must contain markdown table syntax for comparison table"
        )


class TestSuitabilityRatings:
    """Verify suitability ratings are present in comparison table."""

    def test_should_contain_suitability_ratings_when_comparison_table_exists(self, guide_content):
        pattern = re.compile(r'suitability|rating|score|fit', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Comparison table must include suitability ratings or scores"
        )

    def test_should_rate_across_key_dimensions_when_comparison_table_exists(self, guide_content):
        """Verify multiple dimensions are rated, not just a single score."""
        dimension_patterns = [
            re.compile(r'capital|funding\s+amount', re.IGNORECASE),
            re.compile(r'timeline|speed', re.IGNORECASE),
            re.compile(r'equity|ownership|dilution', re.IGNORECASE),
        ]
        matches = sum(1 for p in dimension_patterns if p.search(guide_content))
        assert matches >= 2, (
            f"Comparison table must rate across multiple key dimensions, "
            f"found {matches}/3 expected dimension types"
        )


class TestPlainLanguageExplanation:
    """Verify plain-language explanation for ambiguous results."""

    def test_should_contain_ambiguous_result_explanation_when_guide_loaded(self, guide_content):
        pattern = re.compile(
            r'ambiguous|conflicting|unclear|no\s+clear\s+(winner|top|best)',
            re.IGNORECASE
        )
        assert pattern.search(guide_content), (
            "Guide must contain plain-language explanation for ambiguous results"
        )

    def test_should_contain_guidance_on_reconsidering_inputs_when_ambiguous(self, guide_content):
        pattern = re.compile(
            r'reconsider|revisit|adjust|refine|clarif',
            re.IGNORECASE
        )
        assert pattern.search(guide_content), (
            "Ambiguous results section must guide users on which inputs to reconsider"
        )

    def test_should_handle_conflicting_preferences_scenario_when_guide_loaded(self, guide_content):
        """Verify the specific boundary case of conflicting preferences is addressed."""
        pattern = re.compile(r'conflicting|contradict', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Guide must address the conflicting preferences boundary scenario"
        )
