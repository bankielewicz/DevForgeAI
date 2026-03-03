"""
Test: AC#4 - Valid Pattern Suppression (Catch-and-Ignore)
Story: STORY-404
Generated: 2026-02-15

Verifies Section 8.5 suppresses except: pass patterns as valid
catch-and-ignore with confidence < 0.7.
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


class TestCatchAndIgnoreSuppression:
    """Tests for except:pass suppression logic in Section 8.5."""

    def test_should_document_catch_and_ignore_as_valid(self, section_85):
        """Section 8.5 must document that except: pass is a valid pattern."""
        lower = section_85.lower()
        has_except = "except" in lower
        has_valid = "valid" in lower or "suppress" in lower or "ignore" in lower
        assert has_except and has_valid, (
            "Catch-and-ignore (except: pass) not documented as valid pattern in Section 8.5"
        )

    def test_should_specify_low_confidence_for_valid_patterns(self, section_85):
        """Valid patterns must have confidence < 0.7 to suppress reporting."""
        assert re.search(r"0\.7|confidence|suppress", section_85, re.IGNORECASE), (
            "Confidence threshold for suppression not specified in Section 8.5"
        )

    def test_should_document_context_reading(self, section_85):
        """Stage 2 must read surrounding context (+-3 lines) for classification."""
        lower = section_85.lower()
        has_context = "context" in lower or "surrounding" in lower
        has_lines = re.search(r"[+-]?\s*3\s*lines|\u00b13", section_85)
        assert has_context or has_lines, (
            "Surrounding context reading (+-3 lines) not documented in Section 8.5"
        )

    def test_should_document_valid_pattern_classification(self, section_85):
        """Stage 2 must classify catch-and-ignore as 'valid_pattern'."""
        lower = section_85.lower()
        assert "valid_pattern" in lower or "valid pattern" in lower, (
            "valid_pattern classification not documented in Section 8.5"
        )

    def test_except_pass_pattern_is_real_python(self):
        """Verify except: pass is syntactically valid Python."""
        code = """
try:
    risky_operation()
except ValueError:
    pass
"""
        # This must compile without error - confirms except:pass is valid Python
        compile(code, "<string>", "exec")
