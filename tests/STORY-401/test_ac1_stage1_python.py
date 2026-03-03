"""
Test: AC#1 - Stage 1 Grep Pattern Detection (Python)
Story: STORY-401
Generated: 2026-02-14

Validates that Stage 1 Grep patterns correctly identify commented-out Python code.
These tests will FAIL until the commented-out code detection patterns are added
to .claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md
"""
import re
import pytest


# === Fixture: Load patterns from reference file ===

def load_python_stage1_patterns():
    """
    Load Python Stage 1 Grep patterns from the two-stage-filter-patterns.md reference.
    Returns a list of compiled regex patterns for commented-out Python code detection.

    This function reads the reference file and extracts patterns from the
    'Commented-Out Code Detection' section, specifically the Python Stage 1 patterns.
    """
    import os

    reference_path = os.path.join(
        os.path.dirname(__file__),
        "..", "..",
        ".claude", "agents", "anti-pattern-scanner",
        "references", "two-stage-filter-patterns.md"
    )
    reference_path = os.path.normpath(reference_path)

    if not os.path.exists(reference_path):
        pytest.fail(
            f"Reference file not found: {reference_path}. "
            "Commented-out code patterns must be added to two-stage-filter-patterns.md"
        )

    with open(reference_path, "r") as f:
        content = f.read()

    # Look for Python commented-out code patterns section
    # Expected format: patterns defined under a section like
    # "## Commented-Out Code Detection" > "### Python Stage 1 Patterns"
    # containing regex patterns for commented-out Python code
    python_pattern_section = _extract_python_patterns(content)

    if not python_pattern_section:
        pytest.fail(
            "Python commented-out code Stage 1 patterns not found in "
            "two-stage-filter-patterns.md. Expected section with Python "
            "Grep patterns for commented-out code detection."
        )

    return python_pattern_section


def _extract_python_patterns(content: str) -> list:
    """
    Extract Python Stage 1 patterns from reference file content.
    Looks for patterns matching commented-out Python code keywords.
    Returns list of compiled regex patterns.
    """
    # The reference file should contain patterns like:
    # ^\\s*#\\s*(def |class |import |from |return |if |for |while |try:|except)
    patterns = []

    # Search for the commented-out code section
    if "commented" not in content.lower() or "python" not in content.lower():
        return []

    # Extract regex patterns from code blocks within the Python section
    code_block_pattern = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
    blocks = code_block_pattern.findall(content)

    for block in blocks:
        # Look for lines that look like Grep patterns for Python comments
        for line in block.strip().split("\n"):
            line = line.strip()
            if line.startswith("^") and "#" in line:
                try:
                    compiled = re.compile(line)
                    patterns.append(compiled)
                except re.error:
                    pass

    return patterns


# === Test Constants: Expected match/no-match samples ===

PYTHON_COMMENTED_CODE_SAMPLES = [
    # (input_line, should_match, description)
    ("# def calculate_total(items):", True, "Commented-out function definition"),
    ("# class UserModel:", True, "Commented-out class definition"),
    ("# import os", True, "Commented-out import statement"),
    ("# from pathlib import Path", True, "Commented-out from-import statement"),
    ("# return total * tax_rate", True, "Commented-out return statement"),
    ("# if user.is_active:", True, "Commented-out if statement"),
    ("# for item in cart:", True, "Commented-out for loop"),
    ("# while count < max_retries:", True, "Commented-out while loop"),
    ("# try:", True, "Commented-out try block"),
    ("# except ValueError:", True, "Commented-out except clause"),
    ("    # def helper_method(self):", True, "Indented commented-out function"),
    ("  # class InnerClass:", True, "Indented commented-out class"),
    ("  #   import json", True, "Indented with extra spaces after hash"),
]

PYTHON_NON_CODE_COMMENTS = [
    # (input_line, should_match, description)
    ("# This is a regular comment", False, "Regular prose comment"),
    ("# TODO: fix this later", False, "TODO comment"),
    ("# FIXME: memory leak here", False, "FIXME comment"),
    ("# NOTE: performance optimization", False, "NOTE comment"),
    ("# See documentation at https://example.com", False, "Documentation link"),
    ("# Author: John Doe", False, "Author attribution"),
    ("# Version: 1.2.3", False, "Version comment"),
    ("x = 5  # inline comment", False, "Inline comment after code"),
]


# === Unit Tests ===

class TestPythonStage1PatternLoading:
    """Tests that Python Stage 1 patterns can be loaded from reference file."""

    def test_should_load_patterns_when_reference_file_exists(self):
        """Patterns should load successfully from two-stage-filter-patterns.md."""
        patterns = load_python_stage1_patterns()
        assert len(patterns) > 0, (
            "No Python Stage 1 patterns found. Expected at least one pattern "
            "for commented-out Python code detection."
        )

    def test_should_have_minimum_pattern_count_when_loaded(self):
        """Should have patterns covering def, class, import, from, return, if, for, while, try, except."""
        patterns = load_python_stage1_patterns()
        # At minimum, need patterns for the 10 Python keywords specified in AC#1
        assert len(patterns) >= 1, (
            "Expected at least 1 compiled pattern covering Python keywords. "
            "The pattern should match: def, class, import, from, return, if, for, while, try:, except"
        )


class TestPythonStage1PatternMatching:
    """Tests that patterns correctly match commented-out Python code."""

    @pytest.fixture
    def patterns(self):
        return load_python_stage1_patterns()

    @pytest.mark.parametrize(
        "input_line,should_match,description",
        PYTHON_COMMENTED_CODE_SAMPLES,
        ids=[s[2] for s in PYTHON_COMMENTED_CODE_SAMPLES],
    )
    def test_should_match_commented_code_when_pattern_applied(
        self, patterns, input_line, should_match, description
    ):
        """Pattern should match lines that are commented-out Python code."""
        matched = any(p.search(input_line) for p in patterns)
        assert matched == should_match, (
            f"Pattern {'should' if should_match else 'should not'} match: "
            f"'{input_line}' ({description})"
        )

    @pytest.mark.parametrize(
        "input_line,should_match,description",
        PYTHON_NON_CODE_COMMENTS,
        ids=[s[2] for s in PYTHON_NON_CODE_COMMENTS],
    )
    def test_should_not_match_regular_comments_when_pattern_applied(
        self, patterns, input_line, should_match, description
    ):
        """Pattern should NOT match regular prose comments, TODOs, or inline comments."""
        matched = any(p.search(input_line) for p in patterns)
        assert matched == should_match, (
            f"Pattern should not match non-code comment: "
            f"'{input_line}' ({description})"
        )


class TestPythonStage1PatternCompilation:
    """Tests that all patterns are valid regex."""

    def test_should_compile_all_patterns_when_loaded(self):
        """All loaded patterns should be valid compiled regex objects."""
        patterns = load_python_stage1_patterns()
        for pattern in patterns:
            assert hasattr(pattern, "search"), (
                f"Pattern {pattern} is not a compiled regex object"
            )

    def test_should_handle_multiline_input_when_scanning(self):
        """Patterns should work on individual lines extracted from multiline input."""
        patterns = load_python_stage1_patterns()
        multiline_input = """
# This is a module docstring
# def old_function():
#     pass
# class DeprecatedClass:
#     pass
def active_function():
    pass
"""
        lines = multiline_input.strip().split("\n")
        matches = []
        for line in lines:
            if any(p.search(line) for p in patterns):
                matches.append(line.strip())

        assert "# def old_function():" in matches, (
            "Should match '# def old_function():' in multiline input"
        )
        assert "# class DeprecatedClass:" in matches, (
            "Should match '# class DeprecatedClass:' in multiline input"
        )


class TestPythonStage1EdgeCases:
    """Tests edge cases for Python pattern detection."""

    @pytest.fixture
    def patterns(self):
        return load_python_stage1_patterns()

    def test_should_match_deeply_indented_commented_code_when_nested(self, patterns):
        """Should match commented-out code at any indentation level."""
        deeply_indented = "        # def deeply_nested():"
        matched = any(p.search(deeply_indented) for p in patterns)
        assert matched, "Should match deeply indented commented-out function"

    def test_should_match_tab_indented_commented_code_when_tabs_used(self, patterns):
        """Should match commented-out code with tab indentation."""
        tab_indented = "\t# def tab_indented():"
        matched = any(p.search(tab_indented) for p in patterns)
        assert matched, "Should match tab-indented commented-out function"

    def test_should_not_match_shebang_line_when_at_file_start(self, patterns):
        """Should not match shebang lines like #!/usr/bin/env python."""
        shebang = "#!/usr/bin/env python3"
        matched = any(p.search(shebang) for p in patterns)
        assert not matched, "Should not match shebang line"

    def test_should_not_match_empty_comment_when_hash_only(self, patterns):
        """Should not match bare hash comments."""
        empty_comment = "#"
        matched = any(p.search(empty_comment) for p in patterns)
        assert not matched, "Should not match empty comment"
