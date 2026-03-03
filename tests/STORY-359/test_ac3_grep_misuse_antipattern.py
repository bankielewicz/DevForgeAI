"""
STORY-359 AC#3: Anti-Pattern for Using Grep When Treelint Available

Tests that a FORBIDDEN anti-pattern is documented within Category 11 showing:
- Wrong example: Using Grep for Python/TypeScript/JavaScript/Rust/Markdown
  semantic search when Treelint is available
- Correct example: Using Treelint search/map/deps with --format json
- Rationale citing 99.93% token reduction from ADR-013/RESEARCH-007

TDD Red Phase: These tests WILL FAIL because the Grep misuse anti-pattern
does not exist yet in anti-patterns.md.
"""
import re

import pytest
from pathlib import Path


ANTI_PATTERNS_FILE = Path(
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/anti-patterns.md"
)


def _get_category_11_content() -> str:
    """Extract Category 11 content from anti-patterns.md."""
    content = ANTI_PATTERNS_FILE.read_text()
    cat11_pos = content.find("### Category 11:")
    if cat11_pos == -1:
        pytest.fail("Category 11 not found in anti-patterns.md")
    cat11_content = content[cat11_pos:]
    protocol_pos = cat11_content.find("## Anti-Pattern Detection Protocol")
    if protocol_pos != -1:
        cat11_content = cat11_content[:protocol_pos]
    return cat11_content


class TestAC3GrepMisuseAntiPattern:
    """AC#3: FORBIDDEN block for using Grep when Treelint is available."""

    # --- Happy Path ---

    def test_should_contain_second_forbidden_block_for_grep_misuse(self):
        """Category 11 must contain at least 2 FORBIDDEN blocks (AC#2 + AC#3)."""
        cat11 = _get_category_11_content()
        forbidden_count = cat11.count("FORBIDDEN")
        assert forbidden_count >= 2, (
            f"Expected at least 2 FORBIDDEN blocks in Category 11, found {forbidden_count}. "
            "Need one for unsupported types (AC#2) and one for Grep misuse (AC#3)."
        )

    def test_should_show_wrong_example_using_grep_for_supported_languages(self):
        """Wrong example must show Grep used for supported language semantic search."""
        cat11 = _get_category_11_content()
        lower = cat11.lower()
        # Must mention Grep in a wrong context with supported languages
        has_grep_wrong = "grep" in lower and (
            ".py" in cat11 or "python" in lower or
            ".ts" in cat11 or "typescript" in lower
        )
        assert has_grep_wrong, (
            "Wrong example must show Grep used for supported language files "
            "(e.g., .py, .ts) when Treelint is available"
        )

    def test_should_show_correct_example_using_treelint_commands(self):
        """Correct example must show Treelint search/map/deps commands."""
        cat11 = _get_category_11_content()
        # Must reference treelint commands
        treelint_commands = ["treelint search", "treelint map", "treelint deps"]
        found = [cmd for cmd in treelint_commands if cmd in cat11.lower()]
        assert len(found) >= 1, (
            f"Correct example must show Treelint commands (search/map/deps). "
            f"Found: {found}"
        )

    def test_should_show_format_json_flag_in_correct_example(self):
        """Correct example must include --format json flag."""
        cat11 = _get_category_11_content()
        assert "--format json" in cat11, (
            "Correct example must include '--format json' flag for AI consumption"
        )

    def test_should_cite_adr_013_in_rationale(self):
        """Rationale must cite ADR-013 (Treelint Integration)."""
        cat11 = _get_category_11_content()
        assert "ADR-013" in cat11, (
            "Rationale must cite ADR-013 (Treelint Integration decision)"
        )

    def test_should_cite_research_007_in_rationale(self):
        """Rationale must cite RESEARCH-007 (token reduction evidence)."""
        cat11 = _get_category_11_content()
        assert "RESEARCH-007" in cat11, (
            "Rationale must cite RESEARCH-007 (token reduction research)"
        )

    def test_should_cite_token_reduction_percentage(self):
        """Rationale must cite the 99.93% token reduction figure."""
        cat11 = _get_category_11_content()
        assert "99.93%" in cat11, (
            "Rationale must cite '99.93%' token reduction from ADR-013/RESEARCH-007"
        )

    # --- Edge Cases ---

    def test_should_acknowledge_grep_valid_for_simple_text_patterns(self):
        """Must note that Grep remains valid for simple text patterns even in
        supported languages (e.g., searching for TODO comments)."""
        cat11 = _get_category_11_content()
        lower = cat11.lower()
        # Should mention that Grep is valid for text/simple patterns
        text_pattern_ref = (
            "text" in lower and "pattern" in lower
        ) or (
            "simple" in lower
        ) or (
            "fallback" in lower
        )
        assert text_pattern_ref, (
            "Must acknowledge Grep remains valid for simple text patterns "
            "even in supported languages"
        )

    def test_should_note_treelint_unavailable_fallback(self):
        """Must note that Grep is correct when Treelint is unavailable."""
        cat11 = _get_category_11_content()
        lower = cat11.lower()
        assert "unavailable" in lower or "fallback" in lower or "not installed" in lower, (
            "Must document that Grep is the correct fallback when Treelint is unavailable"
        )
