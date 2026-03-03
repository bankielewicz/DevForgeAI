"""
STORY-359 AC#4: Treelint Recommended Languages Documented

Tests that Category 11 explicitly lists all 5 supported languages with their
file extensions: Python (.py), TypeScript (.ts, .tsx), JavaScript (.js, .jsx),
Rust (.rs), and Markdown (.md). Also verifies that Grep is recommended for all
other languages, simple text-pattern searches, and as fallback when Treelint
is unavailable.

TDD Red Phase: These tests WILL FAIL because the supported languages list
does not exist yet in anti-patterns.md Category 11.
"""
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


class TestAC4SupportedLanguages:
    """AC#4: All 5 Treelint-supported languages documented with extensions."""

    # --- Language Names ---

    def test_should_list_python_as_supported(self):
        """Python must be listed as a Treelint-supported language."""
        cat11 = _get_category_11_content()
        assert "Python" in cat11, "Python not listed as supported language"

    def test_should_list_typescript_as_supported(self):
        """TypeScript must be listed as a Treelint-supported language."""
        cat11 = _get_category_11_content()
        assert "TypeScript" in cat11, "TypeScript not listed as supported language"

    def test_should_list_javascript_as_supported(self):
        """JavaScript must be listed as a Treelint-supported language."""
        cat11 = _get_category_11_content()
        assert "JavaScript" in cat11, "JavaScript not listed as supported language"

    def test_should_list_rust_as_supported(self):
        """Rust must be listed as a Treelint-supported language."""
        cat11 = _get_category_11_content()
        assert "Rust" in cat11, "Rust not listed as supported language"

    def test_should_list_markdown_as_supported(self):
        """Markdown must be listed as a Treelint-supported language."""
        cat11 = _get_category_11_content()
        assert "Markdown" in cat11, "Markdown not listed as supported language"

    # --- File Extensions ---

    def test_should_include_py_extension(self):
        """Must include .py file extension for Python."""
        cat11 = _get_category_11_content()
        assert ".py" in cat11, "Missing .py extension for Python"

    def test_should_include_ts_extension(self):
        """Must include .ts file extension for TypeScript."""
        cat11 = _get_category_11_content()
        assert ".ts" in cat11, "Missing .ts extension for TypeScript"

    def test_should_include_tsx_extension(self):
        """Must include .tsx file extension for TypeScript."""
        cat11 = _get_category_11_content()
        assert ".tsx" in cat11, "Missing .tsx extension for TypeScript"

    def test_should_include_js_extension(self):
        """Must include .js file extension for JavaScript."""
        cat11 = _get_category_11_content()
        assert ".js" in cat11, "Missing .js extension for JavaScript"

    def test_should_include_jsx_extension(self):
        """Must include .jsx file extension for JavaScript."""
        cat11 = _get_category_11_content()
        assert ".jsx" in cat11, "Missing .jsx extension for JavaScript"

    def test_should_include_rs_extension(self):
        """Must include .rs file extension for Rust."""
        cat11 = _get_category_11_content()
        assert ".rs" in cat11, "Missing .rs extension for Rust"

    def test_should_include_md_extension(self):
        """Must include .md file extension for Markdown."""
        cat11 = _get_category_11_content()
        assert ".md" in cat11, "Missing .md extension for Markdown"

    # --- Grep Recommendations ---

    def test_should_recommend_grep_for_unsupported_languages(self):
        """Must explicitly state Grep is recommended for unsupported languages."""
        cat11 = _get_category_11_content()
        lower = cat11.lower()
        assert "grep" in lower, (
            "Must recommend Grep for unsupported languages"
        )

    def test_should_note_grep_for_simple_text_searches(self):
        """Must state Grep is valid for simple text-pattern searches."""
        cat11 = _get_category_11_content()
        lower = cat11.lower()
        has_text_ref = "text" in lower and ("pattern" in lower or "search" in lower)
        assert has_text_ref, (
            "Must note Grep is valid for simple text-pattern searches"
        )

    def test_should_note_grep_as_fallback_when_treelint_unavailable(self):
        """Must state Grep is the fallback when Treelint is unavailable."""
        cat11 = _get_category_11_content()
        lower = cat11.lower()
        assert "unavailable" in lower or "fallback" in lower or "not installed" in lower, (
            "Must note Grep as fallback when Treelint is unavailable"
        )

    # --- Cross-Reference Consistency (BR-004) ---

    def test_should_list_exactly_five_supported_languages(self):
        """Exactly 5 languages must be listed (matching tech-stack.md lines 139-147)."""
        cat11 = _get_category_11_content()
        languages = ["Python", "TypeScript", "JavaScript", "Rust", "Markdown"]
        found = [lang for lang in languages if lang in cat11]
        assert len(found) == 5, (
            f"Expected exactly 5 supported languages, found {len(found)}: {found}. "
            f"Missing: {set(languages) - set(found)}"
        )
