"""
Test: AC#2 - ASCII Chart with Revenue and Cost Lines
Story: STORY-550
Generated: 2026-03-05

Tests validate that break-even-analysis.md specifies:
- Revenue line in ASCII chart
- Total cost line (fixed + variable)
- Break-even intersection marked with distinct symbol
- Labeled axes (x: Units, y: Amount $)
- 80-character width constraint
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
# Chart specification elements
# ---------------------------------------------------------------------------

class TestRevenueLineSpec:
    """Chart must specify a revenue line."""

    def test_should_specify_revenue_line_in_chart(self, reference_content):
        """AC2: Chart must include a revenue line."""
        assert re.search(
            r"revenue\s+(line|curve)", reference_content, re.IGNORECASE
        ), "Chart spec must define a revenue line"

    def test_should_specify_revenue_line_symbol(self, reference_content):
        """AC2: Revenue line must have a distinct character/symbol."""
        # Expect something like "Revenue line: /" or "symbol: R"
        assert re.search(
            r"revenue.*[:\-]\s*[`'\"]?[^\s]", reference_content, re.IGNORECASE
        ), "Revenue line must specify a rendering symbol"


class TestTotalCostLineSpec:
    """Chart must specify a total cost line (fixed + variable)."""

    def test_should_specify_total_cost_line_in_chart(self, reference_content):
        """AC2: Chart must include a total cost line."""
        assert re.search(
            r"(total\s+cost|cost\s+line|fixed\s*\+\s*variable)",
            reference_content,
            re.IGNORECASE,
        ), "Chart spec must define a total cost line"

    def test_should_specify_cost_line_symbol(self, reference_content):
        """AC2: Cost line must have a distinct character/symbol."""
        assert re.search(
            r"cost.*[:\-]\s*[`'\"]?[^\s]", reference_content, re.IGNORECASE
        ), "Cost line must specify a rendering symbol"


class TestBreakEvenIntersection:
    """Break-even intersection must be marked with a distinct symbol."""

    def test_should_specify_intersection_marker(self, reference_content):
        """AC2: Intersection must use a distinct symbol (e.g., X or *)."""
        assert re.search(
            r"(intersection|break.even\s+(point|marker)).*[`'\"]?[X*+#][`'\"]?",
            reference_content,
            re.IGNORECASE,
        ), "Break-even intersection must be marked with a distinct symbol"

    def test_should_differentiate_intersection_from_lines(self, reference_content):
        """AC2: Intersection symbol must differ from line symbols."""
        assert re.search(
            r"(distinct|different|unique|special)\s+(symbol|marker|character)",
            reference_content,
            re.IGNORECASE,
        ), "Intersection marker must be described as distinct from line symbols"


class TestAxisLabels:
    """Chart must have labeled axes."""

    def test_should_label_x_axis_as_units(self, reference_content):
        """AC2: X-axis must be labeled 'Units'."""
        assert re.search(
            r"x.axis.*units", reference_content, re.IGNORECASE
        ), "X-axis must be labeled 'Units'"

    def test_should_label_y_axis_as_amount(self, reference_content):
        """AC2: Y-axis must be labeled 'Amount' or '$'."""
        assert re.search(
            r"y.axis.*(amount|\$|dollar|revenue)", reference_content, re.IGNORECASE
        ), "Y-axis must be labeled with Amount/$"


class TestChartWidthConstraint:
    """Chart must fit within 80 characters width."""

    def test_should_specify_80_char_width(self, reference_content):
        """AC2: Chart must specify 80-character width constraint."""
        assert re.search(
            r"80\s*(char|character|col|column)", reference_content, re.IGNORECASE
        ), "Chart must specify 80-character width constraint"

    def test_should_not_exceed_80_chars_in_example(self, reference_content):
        """AC2: Any chart example in the doc must not exceed 80 chars per line."""
        # Find code blocks that look like charts (contain | or + or axis chars)
        in_code_block = False
        chart_lines = []
        for line in reference_content.split("\n"):
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block and ("|" in line or "+" in line or "-" * 5 in line):
                chart_lines.append(line)

        if chart_lines:
            for line in chart_lines:
                assert len(line) <= 80, (
                    f"Chart line exceeds 80 chars ({len(line)}): {line[:80]}..."
                )
        else:
            pytest.fail("No chart example found in reference file")


class TestChartAutoScaling:
    """Chart must handle auto-scaling for high break-even values."""

    def test_should_document_auto_scaling_behavior(self, reference_content):
        """Edge: Chart must auto-scale when break-even exceeds default range."""
        assert re.search(
            r"(auto.scal|scale.*adjust|dynamic.*scale)",
            reference_content,
            re.IGNORECASE,
        ), "Chart must document auto-scaling for high break-even values"
