"""
Test: AC#6 - Value-Based Pricing Collects Perceived Value Inputs and WTP Anchors
Story: STORY-549
Generated: 2026-03-04

Validates that value-based pricing collects perceived value indicators,
WTP anchors, floor price, and generates a price range with disclaimer.
"""
import os
import re
import pytest

FRAMEWORK_FILE = "src/claude/skills/managing-finances/references/pricing-strategy-framework.md"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


@pytest.fixture
def framework_content():
    """Arrange: Read the pricing-strategy-framework.md file content."""
    path = os.path.join(PROJECT_ROOT, FRAMEWORK_FILE)
    assert os.path.exists(path), f"Source file does not exist: {FRAMEWORK_FILE}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestPerceivedValueCollection:
    """Tests that perceived value indicators are collected."""

    def test_should_collect_key_benefits_when_value_based_selected(self, framework_content):
        """AC6: Key benefits must be collected as perceived value input."""
        assert re.search(r"(key\s+)?benefit", framework_content, re.IGNORECASE), (
            "Key benefits input not documented in value-based pricing"
        )

    def test_should_collect_differentiation_factors_when_value_based_selected(self, framework_content):
        """AC6: Differentiation factors must be collected."""
        assert re.search(r"differentiat", framework_content, re.IGNORECASE), (
            "Differentiation factors not documented in value-based pricing"
        )

    def test_should_document_perceived_value_concept_when_framework_loaded(self, framework_content):
        """AC6: Perceived value concept must be explained."""
        assert re.search(r"perceived\s+value", framework_content, re.IGNORECASE), (
            "Perceived value concept not documented in framework"
        )


class TestWTPAnchors:
    """Tests that willingness-to-pay anchors are collected."""

    def test_should_collect_comparable_alternatives_when_value_based_selected(self, framework_content):
        """AC6: Comparable alternatives must be collected as WTP anchor."""
        assert re.search(
            r"(comparable|alternative|similar\s+product|substitute)",
            framework_content,
            re.IGNORECASE,
        ), (
            "Comparable alternatives not documented in value-based pricing"
        )

    def test_should_collect_customer_budget_range_when_value_based_selected(self, framework_content):
        """AC6: Customer segment budget range must be collected."""
        assert re.search(
            r"(budget\s+range|customer\s+segment.*budget|willingness\s+to\s+pay|WTP)",
            framework_content,
            re.IGNORECASE,
        ), (
            "Customer budget range / WTP anchor not documented"
        )

    def test_should_document_wtp_concept_when_framework_loaded(self, framework_content):
        """AC6: Willingness-to-pay concept must be documented."""
        assert re.search(r"willingness[- ]to[- ]pay|WTP", framework_content, re.IGNORECASE), (
            "Willingness-to-pay concept not documented in framework"
        )


class TestFloorPrice:
    """Tests that floor price is collected."""

    def test_should_collect_floor_price_when_value_based_selected(self, framework_content):
        """AC6: Floor price must be collected."""
        assert re.search(r"floor\s+price", framework_content, re.IGNORECASE), (
            "Floor price input not documented in value-based pricing"
        )


class TestPriceRangeGeneration:
    """Tests that a recommended price range is generated."""

    def test_should_generate_price_range_when_inputs_collected(self, framework_content):
        """AC6: Recommended price range must be generated from inputs."""
        assert re.search(r"price\s+range|range\s+of\s+price", framework_content, re.IGNORECASE), (
            "Price range generation not documented in value-based pricing"
        )

    def test_should_include_rationale_with_price_range_when_generated(self, framework_content):
        """AC6: Price range must include rationale."""
        assert re.search(r"rationale", framework_content, re.IGNORECASE), (
            "No rationale documented for price range output"
        )


class TestValueBasedDisclaimer:
    """BR-001: Disclaimer must appear in value-based pricing output."""

    def test_should_include_disclaimer_when_value_based_output_generated(self, framework_content):
        """BR-001: 'not financial advice' disclaimer must be present."""
        assert re.search(r"not\s+financial\s+advice", framework_content, re.IGNORECASE), (
            "Disclaimer 'not financial advice' not found in framework file"
        )
