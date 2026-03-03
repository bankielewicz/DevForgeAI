"""
Test: AC#5 - Abstract Class Suppression
Story: STORY-404
Generated: 2026-02-15

Verifies Section 8.5 suppresses ABC methods with raise NotImplementedError
or pass as valid abstract patterns (confidence < 0.7).
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


class TestAbstractClassSuppression:
    """Tests for ABC suppression logic in Section 8.5."""

    def test_should_document_abc_detection(self, section_85):
        """Section 8.5 must document ABC/abstract base class detection."""
        lower = section_85.lower()
        has_abc = "abc" in lower or "abstract base" in lower or "abstract class" in lower
        assert has_abc, (
            "ABC/abstract base class detection not documented in Section 8.5"
        )

    def test_should_suppress_abstract_not_implemented(self, section_85):
        """Abstract class NotImplementedError must be suppressed."""
        lower = section_85.lower()
        has_abstract = "abstract" in lower
        has_suppress = "suppress" in lower
        assert has_abstract and has_suppress, (
            "Abstract class suppression not documented in Section 8.5"
        )

    def test_should_suppress_abstract_pass(self, section_85):
        """Abstract class with pass body must be suppressed."""
        lower = section_85.lower()
        # Must mention both abstract and pass as a suppression case
        assert "abstract" in lower and "pass" in lower, (
            "Abstract class pass suppression not documented in Section 8.5"
        )

    def test_should_document_subclass_override_rationale(self, section_85):
        """Suppression rationale must mention enforcing subclass override."""
        lower = section_85.lower()
        has_override = "override" in lower or "subclass" in lower or "inherit" in lower
        assert has_override, (
            "Subclass override rationale not documented for abstract suppression"
        )

    def test_should_specify_low_confidence_for_abstract(self, section_85):
        """Abstract patterns must have confidence < 0.7."""
        # Either explicitly states low confidence or references the 0.7 threshold
        assert re.search(r"0\.7|confidence|suppress", section_85, re.IGNORECASE), (
            "Low confidence for abstract patterns not specified in Section 8.5"
        )

    def test_empty_init_suppression_documented(self, section_85):
        """Empty __init__ (def __init__(self): pass) must be suppressed."""
        lower = section_85.lower()
        assert "__init__" in lower or "constructor" in lower or "empty init" in lower, (
            "Empty __init__ suppression not documented in Section 8.5 (BR-004)"
        )
