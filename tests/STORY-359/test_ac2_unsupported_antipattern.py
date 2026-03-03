"""
STORY-359 AC#2: Anti-Pattern for Using Treelint on Unsupported File Types

Tests that a FORBIDDEN anti-pattern is documented within Category 11 showing:
- Wrong example: Using Treelint for unsupported extensions (.cs, .java, .go, .sql)
- Correct example: Using Grep for those file types
- Rationale explaining token waste from error responses
- Severity level assigned

TDD Red Phase: These tests WILL FAIL because the unsupported file types
anti-pattern does not exist yet in anti-patterns.md.
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
    # Limit to Category 11 section only
    protocol_pos = cat11_content.find("## Anti-Pattern Detection Protocol")
    if protocol_pos != -1:
        cat11_content = cat11_content[:protocol_pos]
    return cat11_content


class TestAC2UnsupportedAntiPattern:
    """AC#2: FORBIDDEN block for using Treelint on unsupported file types."""

    # --- Happy Path ---

    def test_should_contain_forbidden_block_for_unsupported_types(self):
        """A FORBIDDEN block must exist for using Treelint on unsupported file types."""
        cat11 = _get_category_11_content()
        # Must have a FORBIDDEN block that references Treelint + unsupported
        assert "FORBIDDEN" in cat11, (
            "No FORBIDDEN block found in Category 11"
        )
        # Look for Treelint in the context of unsupported usage
        lower = cat11.lower()
        assert "treelint" in lower and "unsupported" in lower, (
            "Category 11 missing FORBIDDEN block for Treelint on unsupported file types"
        )

    def test_should_show_wrong_example_with_unsupported_extensions(self):
        """Wrong example must show Treelint used with unsupported extensions."""
        cat11 = _get_category_11_content()
        # Must mention at least some unsupported extensions
        unsupported_extensions = [".cs", ".java", ".go", ".sql"]
        found = [ext for ext in unsupported_extensions if ext in cat11]
        assert len(found) >= 2, (
            f"Wrong example should mention unsupported extensions. "
            f"Found {found} out of {unsupported_extensions}"
        )

    def test_should_show_correct_example_using_grep_for_unsupported(self):
        """Correct example must show Grep usage for unsupported file types."""
        cat11 = _get_category_11_content()
        # Find the Correct section
        correct_pos = cat11.find("**Correct**")
        if correct_pos == -1:
            pytest.fail("No '**Correct**' section found in Category 11")
        correct_section = cat11[correct_pos:]
        # Must reference Grep as the correct tool
        assert "Grep" in correct_section or "grep" in correct_section.lower(), (
            "Correct example must show Grep as the correct tool for unsupported types"
        )

    def test_should_include_rationale_about_token_waste(self):
        """Rationale must explain token waste from error responses."""
        cat11 = _get_category_11_content()
        lower = cat11.lower()
        assert "token" in lower, (
            "Rationale must mention token waste from Treelint errors on unsupported types"
        )

    def test_should_have_severity_for_unsupported_antipattern(self):
        """The unsupported file types anti-pattern must have a severity level."""
        cat11 = _get_category_11_content()
        pattern = re.compile(r"SEVERITY:\s*(CRITICAL|HIGH|MEDIUM)", re.IGNORECASE)
        match = pattern.search(cat11)
        assert match is not None, (
            "Category 11 missing SEVERITY level for unsupported file types anti-pattern"
        )

    # --- Edge Cases ---

    def test_should_reference_treelint_command_in_wrong_example(self):
        """Wrong example must show an actual treelint command invocation."""
        cat11 = _get_category_11_content()
        assert "treelint" in cat11.lower(), (
            "Wrong example must reference 'treelint' command usage"
        )

    def test_should_use_forbidden_marker_symbol(self):
        """Anti-pattern must use the standard forbidden marker symbol."""
        cat11 = _get_category_11_content()
        # Standard marker in anti-patterns.md is the red X emoji
        assert "\u274c" in cat11 or "FORBIDDEN" in cat11, (
            "Anti-pattern must use standard FORBIDDEN marker"
        )
