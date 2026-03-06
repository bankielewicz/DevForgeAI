"""
Test: AC#1 - Decision Tree Produces Ranked Shortlist Based on Inputs
Story: STORY-552
Generated: 2026-03-06

Validates that the funding-options-guide.md contains a decision tree
that accepts business stage, capital need, and equity preference inputs,
produces a ranked shortlist with rationale, and includes dual disclaimers.
"""
import re
import pytest


class TestDecisionTreeInputs:
    """Verify decision tree accepts required input dimensions."""

    def test_should_contain_business_stage_input_when_decision_tree_defined(self, guide_content):
        """Arrange: Guide content loaded
        Act: Search for business stage input references
        Assert: Business stage is a documented input dimension
        """
        pattern = re.compile(r'business\s+stage', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Decision tree must accept 'business stage' as an input dimension"
        )

    def test_should_contain_capital_need_input_when_decision_tree_defined(self, guide_content):
        """Arrange: Guide content loaded
        Act: Search for capital need input references
        Assert: Capital need is a documented input dimension
        """
        pattern = re.compile(r'capital\s+need', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Decision tree must accept 'capital need' as an input dimension"
        )

    def test_should_contain_equity_preference_input_when_decision_tree_defined(self, guide_content):
        """Arrange: Guide content loaded
        Act: Search for equity preference input references
        Assert: Equity preference is a documented input dimension
        """
        pattern = re.compile(r'equity\s+preference', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Decision tree must accept 'equity preference' as an input dimension"
        )


class TestRankedShortlist:
    """Verify ranked shortlist with rationale is produced."""

    def test_should_contain_ranked_shortlist_section_when_guide_loaded(self, guide_content):
        """Arrange: Guide content loaded
        Act: Search for ranked shortlist section
        Assert: A ranked shortlist section exists
        """
        pattern = re.compile(r'ranked\s+shortlist', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Guide must contain a 'ranked shortlist' section or reference"
        )

    def test_should_contain_rationale_for_rankings_when_shortlist_defined(self, guide_content):
        """Arrange: Guide content loaded
        Act: Search for rationale language near ranking content
        Assert: Rationale is provided for rankings
        """
        pattern = re.compile(r'rationale', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Ranked shortlist must include rationale for each ranking"
        )


class TestDualDisclaimer:
    """Verify disclaimer appears at top AND bottom of output template."""

    def test_should_contain_disclaimer_at_top_when_output_template_defined(self, guide_content):
        """Arrange: Guide content loaded
        Act: Check first section for disclaimer
        Assert: Disclaimer appears near the top of the file
        """
        # Disclaimer should be within first 500 characters or first section
        first_chunk = guide_content[:1500]
        pattern = re.compile(r'disclaimer', re.IGNORECASE)
        assert pattern.search(first_chunk), (
            "Disclaimer must appear at the top of the guide/output template"
        )

    def test_should_contain_disclaimer_at_bottom_when_output_template_defined(self, guide_content):
        """Arrange: Guide content loaded
        Act: Check last section for disclaimer
        Assert: Disclaimer appears near the bottom of the file
        """
        last_chunk = guide_content[-1500:]
        pattern = re.compile(r'disclaimer', re.IGNORECASE)
        assert pattern.search(last_chunk), (
            "Disclaimer must appear at the bottom of the guide/output template"
        )

    def test_should_have_at_least_two_disclaimer_occurrences_when_guide_loaded(self, guide_content):
        """Arrange: Guide content loaded
        Act: Count disclaimer section occurrences
        Assert: At least 2 disclaimer sections exist (top and bottom)
        """
        pattern = re.compile(r'disclaimer', re.IGNORECASE)
        matches = pattern.findall(guide_content)
        assert len(matches) >= 2, (
            f"Expected at least 2 disclaimer references, found {len(matches)}"
        )
