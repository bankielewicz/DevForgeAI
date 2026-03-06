"""
Test: AC#4 - Output Written to funding-strategy.md with Valid Markdown,
             All 5 Funding Types, Dual Disclaimer, and Source Reference
Story: STORY-552
Generated: 2026-03-06

Validates that the guide's output template references the correct artifact
path, documents all 5 funding types, includes dual disclaimer, and cites
the source reference file.
"""
import re
import pytest


FUNDING_TYPES = [
    "Bootstrapping",
    "Grants",
    "Angel Investment",
    "Venture Capital",
    "Debt",  # Debt/Loans - match either form
]


class TestOutputArtifactPath:
    """Verify output template references funding-strategy.md."""

    def test_should_reference_funding_strategy_path_when_guide_loaded(self, guide_content):
        pattern = re.compile(r'funding-strategy\.md', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Guide must reference output artifact path 'funding-strategy.md'"
        )


class TestAllFundingTypesDocumented:
    """Verify all 5 funding types are documented."""

    @pytest.mark.parametrize("funding_type", FUNDING_TYPES)
    def test_should_contain_funding_type_when_guide_loaded(self, guide_content, funding_type):
        pattern = re.compile(re.escape(funding_type), re.IGNORECASE)
        assert pattern.search(guide_content), (
            f"Guide must document funding type: {funding_type}"
        )

    def test_should_contain_loans_reference_when_debt_documented(self, guide_content):
        """Debt/Loans should reference both terms."""
        pattern = re.compile(r'loans?', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Guide must reference 'Loans' as part of the Debt/Loans funding type"
        )


class TestDualDisclaimer:
    """Verify disclaimer appears as first and last section."""

    def test_should_have_disclaimer_as_first_section_when_guide_loaded(self, guide_content):
        # First ## section should be or contain disclaimer
        sections = re.split(r'^## ', guide_content, flags=re.MULTILINE)
        # sections[0] is content before first ##, sections[1] is first ## section
        combined_start = (sections[0] + (sections[1] if len(sections) > 1 else "")).lower()
        assert 'disclaimer' in combined_start, (
            "Disclaimer must appear as the first section of the guide"
        )

    def test_should_have_disclaimer_as_last_section_when_guide_loaded(self, guide_content):
        sections = re.split(r'^## ', guide_content, flags=re.MULTILINE)
        last_section = sections[-1].lower() if sections else ""
        assert 'disclaimer' in last_section, (
            "Disclaimer must appear as the last section of the guide"
        )


class TestSourceReference:
    """Verify source reference line cites the guide file."""

    def test_should_contain_source_reference_to_guide_when_loaded(self, guide_content):
        pattern = re.compile(r'funding-options-guide\.md', re.IGNORECASE)
        assert pattern.search(guide_content), (
            "Guide must contain a source reference citing funding-options-guide.md"
        )
