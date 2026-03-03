"""
Test: AC#2 - Stage 1 Grep Pattern Detection (TypeScript/JavaScript)
Story: STORY-401
Generated: 2026-02-14

Validates that Stage 1 Grep patterns correctly identify commented-out TS/JS code.
These tests will FAIL until the commented-out code detection patterns are added
to .claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md
"""
import re
import pytest


# === Fixture: Load patterns from reference file ===

def load_typescript_stage1_patterns():
    """
    Load TypeScript/JavaScript Stage 1 Grep patterns from two-stage-filter-patterns.md.
    Returns a list of compiled regex patterns for commented-out TS/JS code detection.
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

    patterns = _extract_typescript_patterns(content)

    if not patterns:
        pytest.fail(
            "TypeScript/JavaScript commented-out code Stage 1 patterns not found in "
            "two-stage-filter-patterns.md. Expected section with TS/JS "
            "Grep patterns for commented-out code detection."
        )

    return patterns


def _extract_typescript_patterns(content: str) -> list:
    """
    Extract TypeScript/JavaScript Stage 1 patterns from reference file content.
    Returns list of compiled regex patterns.
    """
    patterns = []

    # The reference file should contain patterns for // commented TS/JS code
    if "commented" not in content.lower():
        return []

    # Look for typescript/javascript section
    ts_keywords = ["typescript", "javascript", "ts/js", "ts_js"]
    has_ts_section = any(kw in content.lower() for kw in ts_keywords)
    if not has_ts_section:
        return []

    code_block_pattern = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
    blocks = code_block_pattern.findall(content)

    for block in blocks:
        for line in block.strip().split("\n"):
            line = line.strip()
            if line.startswith("^") and "//" in line:
                try:
                    compiled = re.compile(line)
                    patterns.append(compiled)
                except re.error:
                    pass

    return patterns


# === Test Constants ===

TS_COMMENTED_CODE_SAMPLES = [
    ("// function calculateTotal(items) {", True, "Commented-out function declaration"),
    ("// class UserModel {", True, "Commented-out class declaration"),
    ("// import { Component } from 'react';", True, "Commented-out import statement"),
    ("// export default class App {", True, "Commented-out export statement"),
    ("// return total * taxRate;", True, "Commented-out return statement"),
    ("// const MAX_RETRIES = 5;", True, "Commented-out const declaration"),
    ("// let counter = 0;", True, "Commented-out let declaration"),
    ("// var legacyVar = 'old';", True, "Commented-out var declaration"),
    ("// if (user.isActive) {", True, "Commented-out if statement"),
    ("// for (const item of cart) {", True, "Commented-out for loop"),
    ("  // function helper() {", True, "Indented commented-out function"),
    ("    // class InnerClass {", True, "Indented commented-out class"),
]

TS_NON_CODE_COMMENTS = [
    ("// This is a regular comment", False, "Regular prose comment"),
    ("// TODO: fix this later", False, "TODO comment"),
    ("// FIXME: memory leak", False, "FIXME comment"),
    ("// @see https://docs.example.com", False, "Documentation reference"),
    ("// Author: Jane Doe", False, "Author attribution"),
    ("// eslint-disable-next-line", False, "ESLint directive"),
    ("// @ts-ignore", False, "TypeScript directive"),
    ("x = 5; // inline comment", False, "Inline comment after code"),
]


# === Unit Tests ===

class TestTypeScriptStage1PatternLoading:
    """Tests that TS/JS Stage 1 patterns can be loaded from reference file."""

    def test_should_load_patterns_when_reference_file_exists(self):
        """Patterns should load successfully from two-stage-filter-patterns.md."""
        patterns = load_typescript_stage1_patterns()
        assert len(patterns) > 0, (
            "No TypeScript/JavaScript Stage 1 patterns found."
        )

    def test_should_have_minimum_pattern_count_when_loaded(self):
        """Should cover function, class, import, export, return, const, let, var, if, for."""
        patterns = load_typescript_stage1_patterns()
        assert len(patterns) >= 1, (
            "Expected at least 1 compiled pattern covering TS/JS keywords."
        )


class TestTypeScriptStage1PatternMatching:
    """Tests that patterns correctly match commented-out TS/JS code."""

    @pytest.fixture
    def patterns(self):
        return load_typescript_stage1_patterns()

    @pytest.mark.parametrize(
        "input_line,should_match,description",
        TS_COMMENTED_CODE_SAMPLES,
        ids=[s[2] for s in TS_COMMENTED_CODE_SAMPLES],
    )
    def test_should_match_commented_code_when_pattern_applied(
        self, patterns, input_line, should_match, description
    ):
        """Pattern should match lines that are commented-out TS/JS code."""
        matched = any(p.search(input_line) for p in patterns)
        assert matched == should_match, (
            f"Pattern {'should' if should_match else 'should not'} match: "
            f"'{input_line}' ({description})"
        )

    @pytest.mark.parametrize(
        "input_line,should_match,description",
        TS_NON_CODE_COMMENTS,
        ids=[s[2] for s in TS_NON_CODE_COMMENTS],
    )
    def test_should_not_match_regular_comments_when_pattern_applied(
        self, patterns, input_line, should_match, description
    ):
        """Pattern should NOT match regular prose comments or directives."""
        matched = any(p.search(input_line) for p in patterns)
        assert matched == should_match, (
            f"Pattern should not match non-code comment: "
            f"'{input_line}' ({description})"
        )


class TestTypeScriptStage1EdgeCases:
    """Tests edge cases for TS/JS pattern detection."""

    @pytest.fixture
    def patterns(self):
        return load_typescript_stage1_patterns()

    def test_should_match_deeply_indented_commented_code_when_nested(self, patterns):
        """Should match commented-out code at any indentation level."""
        deeply_indented = "        // function deeplyNested() {"
        matched = any(p.search(deeply_indented) for p in patterns)
        assert matched, "Should match deeply indented commented-out function"

    def test_should_match_tab_indented_commented_code_when_tabs_used(self, patterns):
        """Should match commented-out code with tab indentation."""
        tab_indented = "\t// class TabIndented {"
        matched = any(p.search(tab_indented) for p in patterns)
        assert matched, "Should match tab-indented commented-out class"

    def test_should_not_match_url_in_comment_when_double_slash_in_url(self, patterns):
        """Should not match URLs containing // as false positives."""
        url_comment = "// https://example.com/api/users"
        matched = any(p.search(url_comment) for p in patterns)
        assert not matched, "Should not match URL comments as code"

    def test_should_not_match_triple_slash_directive_when_ts_reference(self, patterns):
        """Should not match TypeScript triple-slash directives."""
        triple_slash = "/// <reference path='types.d.ts' />"
        matched = any(p.search(triple_slash) for p in patterns)
        assert not matched, "Should not match triple-slash TypeScript directives"
