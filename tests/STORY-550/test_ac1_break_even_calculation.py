"""
Test: AC#1 - Break-Even Calculation with Formulas Shown
Story: STORY-550
Generated: 2026-03-05

Tests validate that break-even-analysis.md contains:
- Break-even units formula: ceil(fixed_costs / (price - variable_cost))
- Break-even revenue formula: units * price
- Contribution margin per unit: price - variable_cost
- Contribution margin ratio: (price - variable_cost) / price * 100%
- Each formula shown alongside its computed value (BR-002)
- Ceiling rounding for non-integer units (BR-005)
- No third-party imports (BR-003)
"""

import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REFERENCE_FILE = os.path.join(
    PROJECT_ROOT,
    "src", "claude", "skills", "managing-finances", "references", "break-even-analysis.md",
)


@pytest.fixture
def reference_content():
    """Load break-even-analysis.md content from src/ tree."""
    assert os.path.exists(REFERENCE_FILE), (
        f"Reference file does not exist: {REFERENCE_FILE}"
    )
    with open(REFERENCE_FILE, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Happy-path formula presence
# ---------------------------------------------------------------------------

class TestBreakEvenUnitsFormula:
    """Verify break-even units formula documentation."""

    def test_should_contain_break_even_units_formula_when_reference_loaded(
        self, reference_content
    ):
        """AC1: ceil(fixed_costs / (price - variable_cost)) must appear."""
        pattern = r"ceil\s*\(\s*fixed.costs\s*/\s*\(\s*price\s*-\s*var(iable)?.cost"
        assert re.search(pattern, reference_content, re.IGNORECASE), (
            "Break-even units formula (ceil(fixed_costs/(price-variable_cost))) not found"
        )

    def test_should_contain_units_computed_value_alongside_formula(
        self, reference_content
    ):
        """BR-002: Formula must appear alongside a computed value example."""
        # Expect a worked example showing both formula and numeric result
        assert re.search(
            r"ceil\s*\(.*\)\s*=\s*\d+", reference_content, re.IGNORECASE
        ), "Break-even units formula must show computed value alongside formula"


class TestBreakEvenRevenueFormula:
    """Verify break-even revenue formula documentation."""

    def test_should_contain_revenue_formula_when_reference_loaded(
        self, reference_content
    ):
        """AC1: revenue = units * price must appear."""
        pattern = r"(break.even\s+)?revenue\s*=\s*.*units\s*\*\s*price"
        assert re.search(pattern, reference_content, re.IGNORECASE), (
            "Break-even revenue formula (units * price) not found"
        )

    def test_should_contain_revenue_computed_value_alongside_formula(
        self, reference_content
    ):
        """BR-002: Revenue formula must show computed value."""
        # Look for pattern like "= $X" or "= X" after revenue formula
        assert re.search(
            r"revenue.*=.*\$?\d[\d,]*", reference_content, re.IGNORECASE
        ), "Revenue formula must show computed value alongside formula"


class TestContributionMarginFormula:
    """Verify contribution margin per unit formula."""

    def test_should_contain_contribution_margin_formula_when_reference_loaded(
        self, reference_content
    ):
        """AC1: contribution margin = price - variable_cost."""
        pattern = r"contribution\s+margin.*=.*price\s*-\s*var(iable)?\s*cost"
        assert re.search(pattern, reference_content, re.IGNORECASE), (
            "Contribution margin formula (price - variable_cost) not found"
        )

    def test_should_contain_margin_computed_value_alongside_formula(
        self, reference_content
    ):
        """BR-002: Contribution margin must show computed value."""
        assert re.search(
            r"contribution\s+margin.*=.*\$?\d+", reference_content, re.IGNORECASE
        ), "Contribution margin must show computed value alongside formula"


class TestContributionMarginRatioFormula:
    """Verify contribution margin ratio formula."""

    def test_should_contain_margin_ratio_formula_when_reference_loaded(
        self, reference_content
    ):
        """AC1: ratio = (price - variable_cost) / price * 100%."""
        pattern = r"(margin\s+ratio|contribution.*ratio).*=.*\(.*price\s*-\s*var(iable)?\s*cost.*\)\s*/\s*price"
        assert re.search(pattern, reference_content, re.IGNORECASE), (
            "Contribution margin ratio formula not found"
        )

    def test_should_contain_ratio_as_percentage(self, reference_content):
        """BR-002: Ratio must show percentage value."""
        assert re.search(
            r"(margin\s+ratio|contribution.*ratio).*\d+(\.\d+)?\s*%",
            reference_content,
            re.IGNORECASE,
        ), "Contribution margin ratio must show percentage value"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCaseZeroFixedCosts:
    """Edge case: zero fixed costs yields break-even at 0 units."""

    def test_should_document_zero_fixed_costs_edge_case(self, reference_content):
        """Zero fixed costs should produce 0 break-even units."""
        assert re.search(
            r"(zero|0)\s+(fixed\s+costs?|fixed_costs)",
            reference_content,
            re.IGNORECASE,
        ), "Edge case for zero fixed costs not documented"

    def test_should_show_zero_units_result_for_zero_fixed_costs(self, reference_content):
        """When fixed costs = 0, break-even units = 0."""
        assert re.search(
            r"break.even.*0\s+units", reference_content, re.IGNORECASE
        ), "Zero fixed costs should result in 0 break-even units"


class TestEdgeCaseNonIntegerUnits:
    """Edge case: non-integer units must use ceiling rounding (BR-005)."""

    def test_should_document_ceiling_rounding(self, reference_content):
        """BR-005: Document ceiling rounding for non-integer units."""
        assert re.search(
            r"ceil(ing)?\s+(round|function)", reference_content, re.IGNORECASE
        ), "Ceiling rounding for non-integer units not documented"

    def test_should_show_fractional_and_ceiling_values(self, reference_content):
        """BR-005: Show both exact fractional and ceiling-rounded values."""
        # Expect something like "10.3 -> 11" or "exact: 10.3, rounded: 11"
        assert re.search(
            r"\d+\.\d+.*\d+", reference_content
        ), "Must show both fractional and ceiling-rounded break-even units"


class TestEdgeCaseZeroVariableCost:
    """Edge case: zero variable cost means margin = selling price."""

    def test_should_document_zero_variable_cost(self, reference_content):
        """Document behavior when variable cost is zero."""
        assert re.search(
            r"(zero|0)\s+variable\s+cost", reference_content, re.IGNORECASE
        ), "Edge case for zero variable cost not documented"


class TestEdgeCaseHighBreakEven:
    """Edge case: high break-even exceeding chart scale."""

    def test_should_document_high_break_even_handling(self, reference_content):
        """Document auto-scaling when break-even is very high."""
        assert re.search(
            r"(auto.scal|scale.*adjust|exceed.*chart|chart.*scale)",
            reference_content,
            re.IGNORECASE,
        ), "High break-even chart scaling not documented"


# ---------------------------------------------------------------------------
# Business rules
# ---------------------------------------------------------------------------

class TestNoThirdPartyImports:
    """BR-003: No third-party library imports."""

    def test_should_specify_stdlib_only(self, reference_content):
        """BR-003: Reference must specify Python stdlib only (math.ceil)."""
        assert re.search(
            r"(stdlib|standard\s+library|math\.ceil|no\s+(third.party|external)\s+(librar|import|depend))",
            reference_content,
            re.IGNORECASE,
        ), "Must specify Python stdlib only / no third-party imports"


class TestFormulaTransparency:
    """BR-002: All 4 formulas must show formula + computed value."""

    def test_should_have_four_formula_value_pairs(self, reference_content):
        """BR-002: At least 4 distinct formula = value patterns."""
        # Count patterns like "formula = value"
        formula_patterns = re.findall(
            r"=\s*\$?\d[\d,.]*", reference_content
        )
        assert len(formula_patterns) >= 4, (
            f"Expected at least 4 formula+value pairs, found {len(formula_patterns)}"
        )
