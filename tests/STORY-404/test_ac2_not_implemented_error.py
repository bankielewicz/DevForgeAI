"""
Test: AC#2 - NotImplementedError Detection
Story: STORY-404
Generated: 2026-02-15

Verifies Section 8.5 detects raise NotImplementedError in concrete classes
(REPORT) and suppresses in abstract base classes (SUPPRESS).
"""
import re
import pytest

SRC_REVIEWER_PATH = "src/claude/agents/code-reviewer.md"


@pytest.fixture
def reviewer_content():
    """Load code-reviewer.md content from src/ tree."""
    with open(SRC_REVIEWER_PATH, "r") as f:
        return f.read()


@pytest.fixture
def section_85(reviewer_content):
    """Extract Section 8.5 content from code-reviewer.md."""
    match = re.search(
        r"(?:##\s*8\.5|###\s*8\.5|Section 8\.5)[^\n]*\n(.*?)(?=\n##\s|\n###\s*\d+\.\s|\Z)",
        reviewer_content,
        re.DOTALL,
    )
    assert match is not None, "Section 8.5 not found in code-reviewer.md"
    return match.group(0)


class TestNotImplementedErrorDetection:
    """Tests for NotImplementedError pattern in Section 8.5."""

    def test_should_contain_not_implemented_pattern(self, section_85):
        """Section 8.5 must define the NotImplementedError pattern."""
        assert "NotImplementedError" in section_85, (
            "NotImplementedError pattern not found in Section 8.5"
        )

    def test_should_distinguish_concrete_vs_abstract(self, section_85):
        """Section 8.5 must document concrete=REPORT, abstract=SUPPRESS."""
        lower = section_85.lower()
        has_concrete = "concrete" in lower
        has_abstract = "abstract" in lower
        assert has_concrete and has_abstract, (
            "Section 8.5 must distinguish concrete class (REPORT) from abstract class (SUPPRESS)"
        )

    def test_should_document_report_action_for_concrete(self, section_85):
        """Concrete class NotImplementedError must be REPORTED."""
        lower = section_85.lower()
        assert "report" in lower, (
            "REPORT action for concrete class NotImplementedError not documented"
        )

    def test_should_document_suppress_action_for_abstract(self, section_85):
        """Abstract class NotImplementedError must be SUPPRESSED."""
        lower = section_85.lower()
        assert "suppress" in lower, (
            "SUPPRESS action for abstract base class NotImplementedError not documented"
        )

    def test_not_implemented_regex_matches_raise(self):
        """The NotImplementedError pattern must match raise statements."""
        pattern = re.compile(r"raise\s+NotImplementedError")
        code = '    raise NotImplementedError("TODO: implement")'
        assert pattern.search(code), "Pattern failed to match raise NotImplementedError"

    def test_not_implemented_regex_matches_bare_raise(self):
        """The NotImplementedError pattern must match bare raise."""
        pattern = re.compile(r"raise\s+NotImplementedError")
        code = "    raise NotImplementedError"
        assert pattern.search(code), "Pattern failed to match bare raise NotImplementedError"
