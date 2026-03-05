"""
Test: AC#2 - Cost-Plus Pricing Collects Inputs, Calculates Price, Displays ASCII Table
Story: STORY-549
Generated: 2026-03-04

Validates cost-plus pricing formula: Price = (VarCost + FixedCost/Units) x (1 + Margin%)
with ASCII table output and disclaimer.
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


class TestCostPlusInputCollection:
    """Tests that cost-plus workflow collects all required inputs."""

    def test_should_collect_variable_cost_when_cost_plus_selected(self, framework_content):
        """AC2: Variable cost per unit input must be collected."""
        assert re.search(r"variable\s+cost", framework_content, re.IGNORECASE), (
            "Variable cost input not documented in framework"
        )

    def test_should_collect_fixed_cost_when_cost_plus_selected(self, framework_content):
        """AC2: Fixed cost input must be collected."""
        assert re.search(r"fixed\s+cost", framework_content, re.IGNORECASE), (
            "Fixed cost input not documented in framework"
        )

    def test_should_collect_unit_volume_when_cost_plus_selected(self, framework_content):
        """AC2: Expected unit volume input must be collected."""
        assert re.search(r"(unit\s+volume|expected\s+units|number\s+of\s+units|units)", framework_content, re.IGNORECASE), (
            "Unit volume input not documented in framework"
        )

    def test_should_collect_margin_percentage_when_cost_plus_selected(self, framework_content):
        """AC2: Target margin percentage input must be collected."""
        assert re.search(r"margin\s*%|margin\s+percentage|target\s+margin", framework_content, re.IGNORECASE), (
            "Margin percentage input not documented in framework"
        )


class TestCostPlusFormula:
    """Tests that the cost-plus formula is correctly documented."""

    def test_should_document_formula_when_cost_plus_section_present(self, framework_content):
        """AC2: Formula Price = (VarCost + FixedCost/Units) x (1 + Margin%) must be documented."""
        # Look for the formula pattern in various notations
        formula_pattern = re.search(
            r"(VarCost|variable\s*cost).*(\+|plus).*FixedCost.*(/|divided|per).*Units.*(\*|x|times|\u00d7).*\(1\s*\+\s*Margin",
            framework_content,
            re.IGNORECASE,
        )
        if not formula_pattern:
            # Try simpler pattern
            formula_pattern = re.search(
                r"Price\s*=\s*\(.*VarCost.*FixedCost.*Units.*\).*\(.*1.*Margin",
                framework_content,
                re.IGNORECASE,
            )
        assert formula_pattern, (
            "Cost-plus formula not found: Price = (VarCost + FixedCost/Units) x (1 + Margin%)"
        )

    def test_should_show_calculation_example_when_formula_documented(self, framework_content):
        """AC2: A worked example or calculation illustration should be present."""
        # Look for numeric example values
        has_numbers = re.search(r"\$?\d+\.?\d*", framework_content)
        assert has_numbers, (
            "No numeric calculation example found in cost-plus section"
        )


class TestCostPlusASCIITable:
    """Tests that cost-plus output includes an ASCII table."""

    def test_should_render_ascii_table_when_cost_plus_calculated(self, framework_content):
        """AC2: ASCII table must show inputs and calculated price."""
        # Look for ASCII table markers (pipes, dashes, plus signs)
        table_pattern = re.search(
            r"(\|[-+]+\||\+[-+]+\+|[\|\+][-\s]+[\|\+])",
            framework_content,
        )
        if not table_pattern:
            # Also accept markdown table format
            table_pattern = re.search(r"\|.*\|.*\|.*\n\|[-: ]+\|", framework_content)
        assert table_pattern, (
            "No ASCII table format found in cost-plus pricing section"
        )

    def test_should_include_inputs_in_table_when_table_rendered(self, framework_content):
        """AC2: Table must include input fields (variable cost, fixed cost, units, margin)."""
        # Find table region and check for input labels
        table_region = re.search(r"\|.*(?:cost|margin|units|price).*\|", framework_content, re.IGNORECASE)
        assert table_region, (
            "ASCII table does not include input/output labels"
        )


class TestCostPlusDisclaimer:
    """BR-001: Disclaimer must appear in cost-plus output."""

    def test_should_include_disclaimer_when_cost_plus_output_generated(self, framework_content):
        """BR-001: 'not financial advice' disclaimer must be in cost-plus section."""
        assert re.search(r"not\s+financial\s+advice", framework_content, re.IGNORECASE), (
            "Disclaimer 'not financial advice' not found in framework file"
        )


class TestCostPlusEdgeCases:
    """Edge case handling for cost-plus pricing."""

    def test_should_warn_on_zero_variable_cost_when_input_is_zero(self, framework_content):
        """Edge: Zero variable cost should trigger warning."""
        assert re.search(r"(zero|0).*cost.*(warn|alert|note|caution)", framework_content, re.IGNORECASE) or \
               re.search(r"(warn|alert|note|caution).*(zero|0).*cost", framework_content, re.IGNORECASE), (
            "No warning for zero variable cost documented"
        )

    def test_should_block_negative_price_when_result_negative(self, framework_content):
        """Edge: Negative price result must block file write."""
        assert re.search(r"negative.*price.*(block|prevent|stop|error)", framework_content, re.IGNORECASE) or \
               re.search(r"(block|prevent|stop|error).*negative.*price", framework_content, re.IGNORECASE), (
            "No handling for negative price result documented"
        )

    def test_should_confirm_implausible_margin_when_above_500_percent(self, framework_content):
        """Edge: Margin > 500% must trigger confirmation prompt."""
        assert re.search(r"500\s*%|implausible.*margin|margin.*confirm", framework_content, re.IGNORECASE), (
            "No handling for implausible margin (>500%) documented"
        )
