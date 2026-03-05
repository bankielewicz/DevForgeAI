"""
Test: AC#1 - Positioning Statement Generation
Story: STORY-540
TDD Phase: Red (tests must FAIL before implementation)

Validates that positioning-strategy.md documents the 3-element positioning
framework (category, differentiation, audience) and the required template.
"""
import re
import pytest


# ---------------------------------------------------------------------------
# BR-001: Positioning statement must contain category, differentiation, audience
# ---------------------------------------------------------------------------

class TestPositioningFrameworkElements:
    """Verify the reference file documents all three framework elements."""

    def test_should_contain_category_element_when_framework_documented(
        self, strategy_content
    ):
        # Arrange - strategy_content loaded by fixture
        # Act & Assert
        assert re.search(r"(?i)category", strategy_content), (
            "Positioning framework must document the 'category' element"
        )

    def test_should_contain_differentiation_element_when_framework_documented(
        self, strategy_content
    ):
        assert re.search(r"(?i)differentiation", strategy_content), (
            "Positioning framework must document the 'differentiation' element"
        )

    def test_should_contain_audience_element_when_framework_documented(
        self, strategy_content
    ):
        assert re.search(r"(?i)audience", strategy_content), (
            "Positioning framework must document the 'audience' element"
        )


# ---------------------------------------------------------------------------
# Template validation
# ---------------------------------------------------------------------------

class TestPositioningTemplate:
    """Verify the standard positioning statement template is documented."""

    def test_should_contain_for_target_audience_template_fragment(
        self, strategy_content
    ):
        # The template starts with "For [target audience]"
        assert re.search(
            r"For\s+\[target\s+audience\]", strategy_content
        ), "Template must include 'For [target audience]' placeholder"

    def test_should_contain_who_need_problem_template_fragment(
        self, strategy_content
    ):
        assert re.search(
            r"who\s+\[need/problem\]", strategy_content
        ), "Template must include 'who [need/problem]' placeholder"

    def test_should_contain_product_is_a_category_template_fragment(
        self, strategy_content
    ):
        assert re.search(
            r"\[product\s+name\]\s+is\s+a\s+\[category\]", strategy_content
        ), "Template must include '[product name] is a [category]' placeholder"

    def test_should_contain_unlike_alternative_template_fragment(
        self, strategy_content
    ):
        assert re.search(
            r"Unlike\s+\[alternative\]", strategy_content
        ), "Template must include 'Unlike [alternative]' placeholder"

    def test_should_contain_primary_differentiator_template_fragment(
        self, strategy_content
    ):
        assert re.search(
            r"\[primary\s+differentiator\]", strategy_content
        ), "Template must include '[primary differentiator]' placeholder"


# ---------------------------------------------------------------------------
# Output section validation
# ---------------------------------------------------------------------------

class TestPositioningOutputSection:
    """Verify the reference documents writing to ## Positioning Statement."""

    def test_should_reference_positioning_statement_section_header(
        self, strategy_content
    ):
        assert re.search(
            r"##\s+Positioning\s+Statement", strategy_content
        ), "Reference must document '## Positioning Statement' output section"
