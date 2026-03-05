"""
Test: AC#3 - Competitive Pricing Integrates EPIC-074 Market Research Data
Story: STORY-549
Generated: 2026-03-04

Validates that competitive pricing reads EPIC-074 data from
competitive-landscape.md and renders a competitor comparison table.
"""
import os
import re
import pytest

FRAMEWORK_FILE = "src/claude/skills/managing-finances/references/pricing-strategy-framework.md"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MARKET_RESEARCH_PATH = "devforgeai/specs/business/market-research/competitive-landscape.md"


@pytest.fixture
def framework_content():
    """Arrange: Read the pricing-strategy-framework.md file content."""
    path = os.path.join(PROJECT_ROOT, FRAMEWORK_FILE)
    assert os.path.exists(path), f"Source file does not exist: {FRAMEWORK_FILE}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestEPIC074Integration:
    """Tests that competitive pricing integrates EPIC-074 market research data."""

    def test_should_reference_competitive_landscape_file_when_competitive_selected(self, framework_content):
        """AC3: Framework must reference the EPIC-074 competitive-landscape.md path."""
        assert re.search(r"competitive-landscape\.md", framework_content, re.IGNORECASE), (
            "No reference to competitive-landscape.md in framework file"
        )

    def test_should_reference_market_research_path_when_reading_data(self, framework_content):
        """AC3: Full or partial path to market research data must be documented."""
        assert re.search(
            r"(market-research|competitive-landscape|EPIC-074)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No reference to market research data source in framework file"
        )

    def test_should_extract_competitor_names_when_data_available(self, framework_content):
        """AC3: Competitor names must be extracted from the data file."""
        assert re.search(r"competitor\s*(name|list|data|pricing)", framework_content, re.IGNORECASE), (
            "No instruction for extracting competitor names from market data"
        )

    def test_should_extract_price_points_when_data_available(self, framework_content):
        """AC3: Competitor price points must be extracted from the data file."""
        assert re.search(r"price\s*point|competitor.*pric", framework_content, re.IGNORECASE), (
            "No instruction for extracting competitor price points"
        )


class TestCompetitorComparisonTable:
    """Tests that a competitor comparison table is rendered."""

    def test_should_render_comparison_table_when_competitive_data_parsed(self, framework_content):
        """AC3: Comparison table must be rendered with competitor data."""
        assert re.search(r"comparison\s*table|competitor\s*table", framework_content, re.IGNORECASE), (
            "No competitor comparison table documented in framework"
        )

    def test_should_include_user_price_in_table_when_comparison_rendered(self, framework_content):
        """AC3: User's proposed price must be positioned relative to competitors."""
        assert re.search(
            r"(your|user|proposed|our)\s*(price|position|pricing)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No user price positioning documented in competitive comparison"
        )

    def test_should_position_user_price_relative_to_competitors_when_table_rendered(self, framework_content):
        """AC3: Framework must document positioning logic (above/below/between)."""
        assert re.search(
            r"(position|rank|relative|above|below|between).*competitor",
            framework_content,
            re.IGNORECASE,
        ) or re.search(
            r"competitor.*(position|rank|relative|above|below|between)",
            framework_content,
            re.IGNORECASE,
        ), (
            "No price positioning logic relative to competitors documented"
        )


class TestCompetitivePricingDisclaimer:
    """BR-001: Disclaimer must appear in competitive pricing output."""

    def test_should_include_disclaimer_in_competitive_output_when_generated(self, framework_content):
        """BR-001: 'not financial advice' disclaimer must be present."""
        assert re.search(r"not\s+financial\s+advice", framework_content, re.IGNORECASE), (
            "Disclaimer 'not financial advice' not found in framework file"
        )
