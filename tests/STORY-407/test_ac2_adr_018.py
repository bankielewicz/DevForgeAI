"""
Test: AC#2 - ADR-018 Created for Catalog Location Decision
Story: STORY-407
Generated: 2026-02-16

Validates that devforgeai/specs/adrs/ADR-018-code-smell-catalog-location.md
contains required ADR sections with proper decision, rationale, and consequences.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ADR_PATH = os.path.join(
    PROJECT_ROOT,
    "devforgeai", "specs", "adrs", "ADR-018-code-smell-catalog-location.md",
)


@pytest.fixture(scope="module")
def adr_content():
    """Read ADR file content."""
    assert os.path.isfile(ADR_PATH), f"ADR-018 file does not exist at {ADR_PATH}"
    with open(ADR_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestADRFileExists:
    """Tests for ADR file existence."""

    def test_should_exist_at_correct_path(self):
        """Assert: ADR-018 file exists at expected path."""
        assert os.path.isfile(ADR_PATH), f"ADR-018 not found at {ADR_PATH}"

    def test_should_be_markdown_format(self, adr_content):
        """Assert: File is valid markdown."""
        assert adr_content.strip().startswith("#"), (
            "ADR file should start with a markdown heading"
        )

    def test_should_contain_adr_018_in_title(self, adr_content):
        """Assert: Title references ADR-018."""
        first_line = adr_content.strip().split("\n")[0]
        assert "ADR-018" in first_line, "Title should contain ADR-018"


class TestADRRequiredSections:
    """Tests for standard ADR sections."""

    def test_should_have_status_section(self, adr_content):
        """Assert: ADR has Status section."""
        assert re.search(r"(?i)##?\s+Status", adr_content), (
            "ADR should have a Status section"
        )

    def test_should_have_context_section(self, adr_content):
        """Assert: ADR has Context section."""
        assert re.search(r"(?i)##?\s+Context", adr_content), (
            "ADR should have a Context section"
        )

    def test_should_have_decision_section(self, adr_content):
        """Assert: ADR has Decision section."""
        assert re.search(r"(?i)##?\s+Decision", adr_content), (
            "ADR should have a Decision section"
        )

    def test_should_have_rationale_section(self, adr_content):
        """Assert: ADR has Rationale section."""
        assert re.search(r"(?i)##?\s+Rationale", adr_content), (
            "ADR should have a Rationale section"
        )

    def test_should_have_consequences_section(self, adr_content):
        """Assert: ADR has Consequences section."""
        assert re.search(r"(?i)##?\s+Consequences", adr_content), (
            "ADR should have a Consequences section"
        )


class TestADRDecisionContent:
    """Tests for decision content specifics."""

    def test_should_decide_reference_file_location(self, adr_content):
        """Assert: Decision places catalog in anti-pattern-scanner references."""
        assert re.search(
            r"(?i)anti.pattern.scanner.*reference", adr_content
        ), "Decision should reference anti-pattern-scanner reference files"

    def test_should_reject_constitutional_anti_patterns_md(self, adr_content):
        """Assert: Decision rejects placing rules in constitutional anti-patterns.md."""
        assert re.search(
            r"(?i)(not|reject|instead of|rather than).*anti.patterns\.md",
            adr_content,
        ), "Decision should explicitly reject constitutional anti-patterns.md"


class TestADRRationale:
    """Tests for rationale content specifics."""

    def test_should_cite_anti_patterns_md_v1_1(self, adr_content):
        """Assert: Rationale cites anti-patterns.md v1.1."""
        assert re.search(r"(?i)anti.patterns\.md.*v1\.1", adr_content), (
            "Rationale should cite anti-patterns.md v1.1"
        )

    def test_should_cite_line_285(self, adr_content):
        """Assert: Rationale cites line 285 distinction."""
        assert "285" in adr_content, (
            "Rationale should cite line 285 of anti-patterns.md"
        )

    def test_should_distinguish_framework_vs_project_patterns(self, adr_content):
        """Assert: Rationale distinguishes framework vs project patterns."""
        assert re.search(
            r"(?i)(framework.*project|project.*framework).*pattern", adr_content
        ), "Rationale should distinguish framework vs project patterns"


class TestADRConsequences:
    """Tests for consequences content."""

    def test_should_document_no_constitutional_modification(self, adr_content):
        """Assert: Consequences state no constitutional file modification."""
        assert re.search(
            r"(?i)(no|without).*(constitutional|LOCKED).*modif", adr_content
        ), "Consequences should state no constitutional file modification"

    def test_should_document_no_locked_status_change(self, adr_content):
        """Assert: Consequences state no LOCKED status change needed."""
        assert re.search(r"(?i)(no|without).*LOCKED.*change", adr_content) or \
               re.search(r"(?i)LOCKED.*status.*(unchanged|remain|preserve)", adr_content), (
            "Consequences should document no LOCKED status change"
        )
