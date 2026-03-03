"""
Test: AC#5 - Multi-Line Comment Block Detection
Story: STORY-401
Generated: 2026-02-14

Validates that multiline comment blocks (/* ... */) containing code keywords
are detected by Stage 1 multiline Grep patterns.
These tests will FAIL until multiline patterns are added to
.claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md
"""
import re
import pytest


# === Fixture: Load multiline patterns from reference file ===

def load_multiline_patterns():
    """
    Load multiline comment block detection patterns from two-stage-filter-patterns.md.
    Returns a list of compiled regex patterns with re.DOTALL for multiline matching.
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
            "Multiline comment block patterns must be added."
        )

    with open(reference_path, "r") as f:
        content = f.read()

    patterns = _extract_multiline_patterns(content)

    if not patterns:
        pytest.fail(
            "Multiline comment block detection patterns for commented-out code "
            "not found in two-stage-filter-patterns.md. Expected patterns like "
            r"/\*[\s\S]*?(function|class|import|return)[\s\S]*?\*/"
        )

    return patterns


def _extract_multiline_patterns(content: str) -> list:
    """
    Extract multiline comment block patterns from reference file content.
    Returns list of compiled regex patterns with DOTALL flag.
    """
    patterns = []
    lower = content.lower()

    # Must relate to commented-out code, not data class
    if "commented" not in lower and "multi-line" not in lower and "multiline" not in lower:
        return []

    # Look for multiline pattern section
    if "multiline" not in lower and "multi-line" not in lower and "block comment" not in lower:
        return []

    # Extract patterns from code blocks
    code_blocks = re.findall(r"```[^\n]*\n(.*?)```", content, re.DOTALL)
    for block in code_blocks:
        for line in block.strip().split("\n"):
            line = line.strip()
            # Look for patterns with /* */ style
            if "/\\*" in line or "/*" in line:
                try:
                    # Try compiling with DOTALL for multiline matching
                    compiled = re.compile(line, re.DOTALL)
                    patterns.append(compiled)
                except re.error:
                    pass

    return patterns


# === Test Constants: Multiline comment samples ===

MULTILINE_CODE_BLOCKS = [
    {
        "name": "Block comment with function",
        "content": """/*
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}
*/""",
        "should_match": True,
    },
    {
        "name": "Block comment with class",
        "content": """/*
class UserModel {
    constructor(name) {
        this.name = name;
    }
}
*/""",
        "should_match": True,
    },
    {
        "name": "Block comment with import",
        "content": """/*
import { Component } from 'react';
import { connect } from 'react-redux';
*/""",
        "should_match": True,
    },
    {
        "name": "Block comment with return",
        "content": """/*
return {
    status: 200,
    data: results
};
*/""",
        "should_match": True,
    },
]

MULTILINE_NON_CODE_BLOCKS = [
    {
        "name": "Regular block comment documentation",
        "content": """/*
This module handles user authentication.
It supports both OAuth and basic auth.
See documentation for configuration options.
*/""",
        "should_match": False,
    },
    {
        "name": "License header block",
        "content": """/*
Copyright (c) 2026 Example Corp.
All rights reserved.
Licensed under MIT.
*/""",
        "should_match": False,
    },
]


# === Unit Tests ===

class TestMultilinePatternLoading:
    """Tests that multiline patterns can be loaded from reference file."""

    def test_should_load_patterns_when_reference_file_exists(self):
        """Multiline patterns should load successfully."""
        patterns = load_multiline_patterns()
        assert len(patterns) > 0, (
            "No multiline comment block patterns found."
        )

    def test_should_have_dotall_capable_patterns_when_loaded(self):
        """Patterns should handle newlines within comment blocks."""
        patterns = load_multiline_patterns()
        # Test that at least one pattern can match across newlines
        test_input = "/* function test() {} */"
        matched = any(p.search(test_input) for p in patterns)
        assert matched, (
            "At least one pattern should match a single-line block comment with code"
        )


class TestMultilineCodeBlockDetection:
    """Tests that multiline code blocks are correctly detected."""

    @pytest.fixture
    def patterns(self):
        return load_multiline_patterns()

    @pytest.mark.parametrize(
        "sample",
        MULTILINE_CODE_BLOCKS,
        ids=[s["name"] for s in MULTILINE_CODE_BLOCKS],
    )
    def test_should_match_code_in_block_comment_when_code_present(
        self, patterns, sample
    ):
        """Block comments containing code keywords should match."""
        matched = any(p.search(sample["content"]) for p in patterns)
        assert matched == sample["should_match"], (
            f"Pattern should match block comment with code: {sample['name']}"
        )

    @pytest.mark.parametrize(
        "sample",
        MULTILINE_NON_CODE_BLOCKS,
        ids=[s["name"] for s in MULTILINE_NON_CODE_BLOCKS],
    )
    def test_should_not_match_documentation_block_when_no_code(
        self, patterns, sample
    ):
        """Block comments with only prose should NOT match."""
        matched = any(p.search(sample["content"]) for p in patterns)
        assert matched == sample["should_match"], (
            f"Pattern should not match non-code block comment: {sample['name']}"
        )


class TestMultilineEdgeCases:
    """Tests edge cases for multiline comment block detection."""

    @pytest.fixture
    def patterns(self):
        return load_multiline_patterns()

    def test_should_match_single_line_block_comment_with_code(self, patterns):
        """Single-line block comment with code keyword should match."""
        single_line = "/* function unused() { return; } */"
        matched = any(p.search(single_line) for p in patterns)
        assert matched, "Should match single-line block comment with function"

    def test_should_match_nested_code_in_block_comment(self, patterns):
        """Block comment with deeply nested code should match."""
        nested = """/*
    function outer() {
        class Inner {
            import { something } from 'module';
        }
    }
*/"""
        matched = any(p.search(nested) for p in patterns)
        assert matched, "Should match nested code in block comment"

    def test_should_not_match_empty_block_comment(self, patterns):
        """Empty block comment should NOT match."""
        empty = "/* */"
        matched = any(p.search(empty) for p in patterns)
        assert not matched, "Should not match empty block comment"

    def test_should_handle_block_comment_with_asterisk_lines(self, patterns):
        """Block comments with * prefix per line should be handled."""
        asterisk_style = """/*
 * function deprecatedHandler() {
 *     return oldResult;
 * }
 */"""
        matched = any(p.search(asterisk_style) for p in patterns)
        assert matched, (
            "Should match block comments with asterisk-prefixed lines containing code"
        )
