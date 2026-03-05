"""
Test: AC#3 - Output Appended to projections.md
Story: STORY-550
Generated: 2026-03-05

Tests validate that break-even-analysis.md specifies:
- Output appended to projections.md
- Heading: "## Break-Even Analysis"
- Timestamp in ISO 8601 format
- Calculated results section
- ASCII chart included
- Assumptions section listing input values
- Disclaimer (BR-001, NFR-S003)
- File creation when projections.md does not exist
- Multiple analyses appended (not overwritten)
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
# Output format specification
# ---------------------------------------------------------------------------

class TestProjectionsHeading:
    """Output must include ## Break-Even Analysis heading."""

    def test_should_specify_break_even_heading(self, reference_content):
        """AC3: Output heading must be '## Break-Even Analysis'."""
        assert re.search(
            r"##\s+Break-Even Analysis", reference_content
        ), "Output must specify '## Break-Even Analysis' heading"


class TestTimestampFormat:
    """Output must include ISO 8601 timestamp."""

    def test_should_specify_iso_8601_timestamp(self, reference_content):
        """AC3: Timestamp must be ISO 8601 format."""
        assert re.search(
            r"ISO\s*8601|timestamp.*ISO|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}",
            reference_content,
            re.IGNORECASE,
        ), "Output must specify ISO 8601 timestamp format"

    def test_should_include_timestamp_in_output_format(self, reference_content):
        """AC3: Timestamp must appear in the output format specification."""
        assert re.search(
            r"timestamp", reference_content, re.IGNORECASE
        ), "Output format must include timestamp"


class TestResultsSection:
    """Output must include calculated results."""

    def test_should_specify_results_in_output(self, reference_content):
        """AC3: Output format must include calculated results."""
        assert re.search(
            r"(results?|calculation)\s*(section|output|display)",
            reference_content,
            re.IGNORECASE,
        ), "Output must specify a results section"


class TestChartInOutput:
    """Output must include the ASCII chart."""

    def test_should_specify_chart_in_output(self, reference_content):
        """AC3: ASCII chart must be included in projections.md output."""
        assert re.search(
            r"(chart|visual).*projections|projections.*chart",
            reference_content,
            re.IGNORECASE,
        ), "ASCII chart must be specified as part of projections.md output"


class TestAssumptionsSection:
    """Output must include assumptions listing input values."""

    def test_should_specify_assumptions_section(self, reference_content):
        """AC3: Output must include assumptions section."""
        assert re.search(
            r"assumptions?\s*(section|list|block)", reference_content, re.IGNORECASE
        ), "Output must specify an assumptions section"

    def test_should_list_input_values_in_assumptions(self, reference_content):
        """AC3: Assumptions must list the input values used."""
        assert re.search(
            r"assumptions?.*(fixed\s+costs?|variable\s+cost|selling\s+price|input)",
            reference_content,
            re.IGNORECASE,
        ), "Assumptions section must list input values (fixed costs, variable cost, price)"


class TestDisclaimerPresence:
    """BR-001 / NFR-S003: Disclaimer must be in every output section."""

    def test_should_specify_disclaimer_in_output(self, reference_content):
        """BR-001: Disclaimer must be included in output."""
        assert re.search(
            r"disclaimer", reference_content, re.IGNORECASE
        ), "Output format must include a disclaimer"

    def test_should_state_estimates_not_advice(self, reference_content):
        """NFR-S003: Disclaimer must note results are estimates, not professional advice."""
        assert re.search(
            r"(estimate|not\s+(professional\s+)?financial\s+advice)",
            reference_content,
            re.IGNORECASE,
        ), "Disclaimer must state results are estimates / not professional financial advice"


class TestProjectionsFileCreation:
    """When projections.md does not exist, it must be created."""

    def test_should_document_file_creation_behavior(self, reference_content):
        """AC3: Document that projections.md is created if missing."""
        assert re.search(
            r"(creat|generat).*projections\.md|projections\.md.*(creat|not\s+exist|missing)",
            reference_content,
            re.IGNORECASE,
        ), "Must document that projections.md is created when missing"


class TestMultipleAnalysesAppended:
    """Multiple analyses must be appended, not overwritten."""

    def test_should_specify_append_behavior(self, reference_content):
        """AC3: Must specify append (not overwrite) for multiple analyses."""
        assert re.search(
            r"append", reference_content, re.IGNORECASE
        ), "Must specify append behavior for projections.md"

    def test_should_preserve_prior_sections(self, reference_content):
        """AC3: Prior sections must be preserved when appending."""
        assert re.search(
            r"(preserv|not\s+overwrit|prior|existing|previous)",
            reference_content,
            re.IGNORECASE,
        ), "Must specify that prior sections are preserved"


class TestOutputPath:
    """Output must target devforgeai/specs/business/financial/projections.md."""

    def test_should_specify_projections_file_path(self, reference_content):
        """AC3: Must specify the projections.md output path."""
        assert re.search(
            r"devforgeai/specs/business/financial/projections\.md",
            reference_content,
        ), "Must specify output path: devforgeai/specs/business/financial/projections.md"
