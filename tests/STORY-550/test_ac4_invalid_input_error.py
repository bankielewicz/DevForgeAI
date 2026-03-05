"""
Test: AC#4 - Error on Invalid Price/Cost Inputs
Story: STORY-550
Generated: 2026-03-05

Tests validate that break-even-analysis.md specifies:
- Error when selling price = variable cost (zero contribution margin)
- Error when selling price < variable cost (negative margin)
- Error when selling price is negative
- Error when fixed costs are negative
- Clear error message explaining contribution margin must be positive
- No output written to projections.md on error (BR-004)
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
# Price = variable cost (zero contribution margin)
# ---------------------------------------------------------------------------

class TestPriceEqualsVariableCost:
    """Error when selling price equals variable cost."""

    def test_should_document_error_when_price_equals_variable_cost(
        self, reference_content
    ):
        """AC4: Must document error for price = variable cost."""
        assert re.search(
            r"(price\s*(=|equals?)\s*var(iable)?\s*cost|zero\s+contribution\s+margin)",
            reference_content,
            re.IGNORECASE,
        ), "Must document error when price equals variable cost"

    def test_should_explain_positive_contribution_margin_required(
        self, reference_content
    ):
        """AC4: Error message must explain contribution margin must be positive."""
        assert re.search(
            r"(contribution\s+margin\s+must\s+be\s+positive|positive\s+contribution\s+margin|price\s+must\s+(exceed|be\s+greater))",
            reference_content,
            re.IGNORECASE,
        ), "Error must explain that contribution margin must be positive"


# ---------------------------------------------------------------------------
# Price < variable cost (negative margin)
# ---------------------------------------------------------------------------

class TestPriceLessThanVariableCost:
    """Error when selling price is less than variable cost."""

    def test_should_document_error_when_price_less_than_variable_cost(
        self, reference_content
    ):
        """AC4: Must document error for price < variable cost."""
        assert re.search(
            r"(price\s*(<|less\s+than|below)\s*var(iable)?\s*cost|negative\s+(contribution\s+)?margin)",
            reference_content,
            re.IGNORECASE,
        ), "Must document error when price is less than variable cost"


# ---------------------------------------------------------------------------
# Negative selling price
# ---------------------------------------------------------------------------

class TestNegativeSellingPrice:
    """Error when selling price is negative."""

    def test_should_document_negative_price_error(self, reference_content):
        """AC4: Must document error for negative selling price."""
        assert re.search(
            r"negative\s+(selling\s+)?price", reference_content, re.IGNORECASE
        ), "Must document error for negative selling price"


# ---------------------------------------------------------------------------
# Negative fixed costs
# ---------------------------------------------------------------------------

class TestNegativeFixedCosts:
    """Error when fixed costs are negative."""

    def test_should_document_negative_fixed_costs_error(self, reference_content):
        """AC4: Must document error for negative fixed costs."""
        assert re.search(
            r"negative\s+fixed\s+costs?", reference_content, re.IGNORECASE
        ), "Must document error for negative fixed costs"


# ---------------------------------------------------------------------------
# No output on error
# ---------------------------------------------------------------------------

class TestNoOutputOnError:
    """No output written to projections.md when errors occur."""

    def test_should_specify_no_write_on_error(self, reference_content):
        """AC4: Must specify that no output is written to projections.md on error."""
        assert re.search(
            r"(no\s+(output|write|append)|not\s+writ|halt.*before.*write|error.*before.*(calculat|output))",
            reference_content,
            re.IGNORECASE,
        ), "Must specify no output is written to projections.md on error"


# ---------------------------------------------------------------------------
# Error message clarity
# ---------------------------------------------------------------------------

class TestErrorMessageClarity:
    """Error messages must be clear and descriptive."""

    def test_should_specify_clear_error_message(self, reference_content):
        """AC4: Must specify clear/descriptive error message."""
        assert re.search(
            r"(clear|descriptive|explain|user.friendly)\s*(error|message)",
            reference_content,
            re.IGNORECASE,
        ), "Must specify clear/descriptive error messages"

    def test_should_provide_error_message_example(self, reference_content):
        """AC4: Must provide example error message text."""
        assert re.search(
            r'(error|message).*["\'].*selling\s+price|["\'].*price.*exceed',
            reference_content,
            re.IGNORECASE,
        ), "Must provide example error message text"
