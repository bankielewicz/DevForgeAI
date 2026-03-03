"""
Test: AC#3 - TypeScript/JavaScript Placeholder Detection
Story: STORY-404
Generated: 2026-02-15

Verifies Section 8.5 detects TS/JS placeholder patterns:
- throw new Error('Not implemented')
- return null; // TODO
- empty blocks {}
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


class TestTypeScriptPlaceholderDetection:
    """Tests for TypeScript/JavaScript placeholder patterns in Section 8.5."""

    def test_should_contain_throw_error_pattern(self, section_85):
        """Section 8.5 must define throw new Error('Not implemented') pattern."""
        assert re.search(r"throw\s+new\s+Error|Not implemented", section_85), (
            "throw new Error('Not implemented') pattern not found in Section 8.5"
        )

    def test_should_contain_return_null_todo_pattern(self, section_85):
        """Section 8.5 must define return null // TODO pattern."""
        lower = section_85.lower()
        has_return_null = "return null" in lower or "return_null" in lower
        has_todo = "todo" in lower
        assert has_return_null and has_todo, (
            "return null // TODO pattern not documented in Section 8.5"
        )

    def test_should_contain_empty_block_pattern(self, section_85):
        """Section 8.5 must define empty block {} detection pattern."""
        has_empty_block = (
            "empty block" in section_85.lower()
            or "empty_block" in section_85.lower()
            or re.search(r"\{\s*\}", section_85)
        )
        assert has_empty_block, (
            "Empty block {} pattern not documented in Section 8.5"
        )

    def test_throw_error_regex_matches(self):
        """The throw Error pattern must match TS/JS throw statements."""
        pattern = re.compile(r"throw\s+new\s+Error\s*\(\s*['\"]Not implemented['\"]\s*\)")
        code = "throw new Error('Not implemented');"
        assert pattern.search(code), "Pattern failed to match throw new Error('Not implemented')"

    def test_return_null_todo_regex_matches(self):
        """The return null TODO pattern must match commented returns."""
        pattern = re.compile(r"return\s+null\s*;\s*//\s*(TODO|FIXME|HACK)")
        code = "return null; // TODO: implement this"
        assert pattern.search(code), "Pattern failed to match return null; // TODO"

    def test_empty_block_regex_matches(self):
        """The empty block pattern must match {} with optional whitespace."""
        pattern = re.compile(r"\{\s*\}")
        assert pattern.search("function process() {}"), "Pattern failed to match empty block {}"
        assert pattern.search("function process() { }"), "Pattern failed to match empty block { }"

    def test_should_reference_typescript_or_javascript(self, section_85):
        """Section 8.5 must reference TypeScript or JavaScript language."""
        lower = section_85.lower()
        assert "typescript" in lower or "javascript" in lower or "ts/js" in lower, (
            "TypeScript/JavaScript not referenced in Section 8.5"
        )
