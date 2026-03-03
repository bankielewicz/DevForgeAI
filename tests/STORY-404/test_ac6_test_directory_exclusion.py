"""
Test: AC#6 - Test Directory Exclusion
Story: STORY-404
Generated: 2026-02-15

Verifies Section 8.5 excludes test directories from placeholder scanning:
tests/, test_*, __tests__/, *.test.ts
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


class TestTestDirectoryExclusion:
    """Tests for test directory exclusion in Section 8.5."""

    def test_should_document_test_directory_exclusion(self, section_85):
        """Section 8.5 must document test directory exclusion."""
        lower = section_85.lower()
        has_exclude = "exclud" in lower or "skip" in lower or "ignore" in lower
        has_test = "test" in lower
        assert has_exclude and has_test, (
            "Test directory exclusion not documented in Section 8.5"
        )

    def test_should_exclude_tests_directory(self, section_85):
        """tests/ directory must be in exclusion list."""
        assert "tests/" in section_85 or "tests/" in section_85.lower(), (
            "tests/ directory not in exclusion list"
        )

    def test_should_exclude_test_prefix(self, section_85):
        """test_* prefix files must be in exclusion list."""
        assert "test_" in section_85, (
            "test_* prefix not in exclusion list"
        )

    def test_should_exclude_dunder_tests(self, section_85):
        """__tests__/ directory must be in exclusion list."""
        assert "__tests__" in section_85, (
            "__tests__/ directory not in exclusion list"
        )

    def test_should_document_exclusion_rationale(self, section_85):
        """Exclusion rationale must mention tests legitimately containing stubs."""
        lower = section_85.lower()
        has_rationale = (
            "legitimate" in lower
            or "stub" in lower
            or "mock" in lower
            or "test files" in lower
        )
        assert has_rationale, (
            "Rationale for test directory exclusion not documented"
        )
